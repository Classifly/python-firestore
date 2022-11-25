from typing import Type, Any

from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.transforms import DELETE_FIELD

class FirestoreProperty(property):
    def __init__(self, db_name:str,object_class:Type):
        def getter(document_reference:DocumentReference):
            raw_val = document_reference.get().to_dict().get(db_name)

            if isinstance(raw_val,object_class):
                return raw_val
            return object_class(raw_val)

        def setter(document_reference:DocumentReference,val:Any):
            #If a cached document snapshot exists, update the cached object to prevent data integrity issues
            if document_reference._document_snapshot is not None:
                document_reference._document_snapshot._data[db_name] = val

            document_reference.update({
                db_name: val
            })

        def deleter(doc_ref:DocumentReference):
            doc_ref.update({
                db_name: DELETE_FIELD
            })
        super().__init__(getter, setter, deleter)
