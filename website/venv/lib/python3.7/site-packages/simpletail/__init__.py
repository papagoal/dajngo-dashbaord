from locale import getpreferredencoding


class ropen(object):
    def __init__(
        self,
        filename,
        bufsize=4096,
        encoding=None,
        errors=None,
        newline=None,
        closefd=True,
    ):
        if bufsize <= 2:
            raise ValueError("{} is not a serious buffer size".format(bufsize))
        self.bufsize = bufsize

        # seek() and tell() don't work well in text files, at least not in
        # Python 3; they need to read all the file and make conversions.
        # We thus open the file in binary mode and make conversions later.
        self.encoding = encoding if encoding else getpreferredencoding()
        self.errors = errors if errors else "strict"
        self.newline = newline

        self.fileobject = open(filename, "rb", buffering=bufsize, closefd=closefd)

        self.fileobject.seek(0, 2)  # Go to end of file
        self.buf = b""

    def close(self):
        self.fileobject.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fileobject.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        return self

    def __next__(self):
        next_line = self.get_next_undecoded_line()
        if self.newline is None:
            next_line = next_line.replace(b"\r\n", b"\n")
            next_line = next_line.replace(b"\r", b"\n")
        return next_line.decode(self.encoding, self.errors)

    def readline(self):
        try:
            return self.__next__()
        except StopIteration:
            return ""

    def get_next_undecoded_line(self):
        start_of_line = self.get_start_of_line()
        if not start_of_line:
            self.read_next_into_buf()
            start_of_line = self.get_start_of_line()
        result = self.buf[start_of_line:]
        self.buf = self.buf[:start_of_line]
        return result

    def get_start_of_line(self):
        """Return index of start of last line stored in self.buf.
        This function never fetches more data from the file; therefore,
        if it returns zero, meaning the line starts at the beginning of the
        buffer, the caller should then fetch more data and retry.
        """
        if self.newline in ("\r", "\n", "\r\n"):
            return self.buf.rfind(self.newline.encode("ascii"), 0, -1) + 1
        if self.newline:
            raise ValueError(
                r"ropen newline argument must be one of "
                r"None, '', '\r', '\n', '\r\n'."
            )

        # self.newline is None or ''; universal newlines mode
        end_of_search = -1
        if len(self.buf) >= 2 and self.buf[-2:] == b"\r\n":
            end_of_search = -2
        return (
            max(
                self.buf.rfind(b"\n", 0, end_of_search),
                self.buf.rfind(b"\r", 0, end_of_search),
            )
            + 1
        )

    def read_next_into_buf(self):
        """Read data from the file in self.bufsize chunks until we're
           certain we have a full line in the buffer.
        """
        file_pos = self.fileobject.tell()
        if (file_pos == 0) and (self.buf == b""):
            raise StopIteration
        while file_pos and (self.get_start_of_line() == 0):
            bytes_to_read = min(self.bufsize, file_pos)
            file_pos = file_pos - bytes_to_read
            self.fileobject.seek(file_pos)
            new_stuff = self.fileobject.read(bytes_to_read)[:bytes_to_read]
            self.fileobject.seek(file_pos)
            self.buf = new_stuff + self.buf
