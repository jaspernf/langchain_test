import hashlib
class Row:
    """Abstraction of one data point."""
    __fields = None

    def __init__(self, fields):
        fields.append("ObjectKey")
        self.__fields = fields
        for field in fields:
            self.__setattr__(field.lower().replace(' ', '_'), "")

    def header(self):
        """
        Returns a list of field names.
        :return: list of column names.in
        :rtype: list
        """
        return self.__fields

    def clear(self):
        for f in self.__fields:
            self.__setattr__(f.lower().replace(' ', '_'), "")

    def values(self):
        """Returns a list of field values"""
        return[self.__getattribute__(f.lower().replace(' ', '_')) for f in self.__fields]

    def compute_key(self):
        """Compute the row's ObjectKey
            :return: ObjectKey, which serves as row id.in
            :rtype: str
        """
        strrep = str(self.values()).encode()
        key = hashlib.sha256(strrep).hexdigest()
        return key