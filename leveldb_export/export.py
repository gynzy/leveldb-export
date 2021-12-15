from io import BytesIO
from typing import Generator, Union

from google.appengine.api.datastore_types import EmbeddedEntity
from google.appengine.datastore import entity_bytes_pb2 as entity_pb2
from google.appengine.api.datastore import Entity

from .records import RecordsReader
from .utils import embedded_entity_to_dict


def parse_entity_field(value):
    """Function for recursive parsing (e.g., arrays)"""

    if isinstance(value, EmbeddedEntity):
        # Some nested document
        return embedded_entity_to_dict(value, {})

    if isinstance(value, list):
        return [parse_entity_field(x) for x in value]

    return value


def parse_leveldb_documents(path_or_fp: Union[str, BytesIO]) -> Generator[dict, None, None]:
    """
    Parses a LevelDB file and returns generator of parsed objects. Objects are returned as parsed
    documents from the file, and augmented with a _key dict containing id, name, path, kind,
    namespace and kind.

    Args:
        - path_or_fp (str | io.BytesIO): path to local file (if str) or an open file pointer.
            Note, if not str it assumes the file is already open and user is responsible
            for closing the file.

    Raises:
        - RuntimeError: if the document contains already contains a _key property.
        - InvalidRecordError: if invalid record is encountered.

    Returns:
        - Generator[dict]: generator returning each distinctive document.
    """

    # Open the file if path was provided
    if isinstance(path_or_fp, str):
        fp = open(path_or_fp, "rb")
    else:
        fp = path_or_fp

    reader = RecordsReader(fp, no_check_crc=True)
    for record in reader:
        # Read the record as entity
        entity_proto = entity_pb2.EntityProto()
        entity_proto.ParseFromString(record)
        entity = Entity.FromPb(entity_proto)

        # Parse the values
        data = {}
        for name, value in entity.items():
            # NOTE: this check is unlikely, if we run into this we could use a different name
            # or make it configurable. At least we will be aware when it happens :)
            if name == "_key":
                raise RuntimeError("Failed to parse document, _key already present.")

            data[name] = parse_entity_field(value)

        key = entity.key()
        data["_key"] = dict(
            id=key.id(),
            name=key.name(),
            namespace=key.namespace(),
            app=key.app(),
            path="/".join(key.to_path()),
        )

        yield data

    # On completion, possibly close the file pointer if we opened it
    if isinstance(path_or_fp, str):
        fp.close()
