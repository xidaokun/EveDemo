MONGO_HOST = 'localhost'
MONGO_PORT = 27017

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

URL_PREFIX = 'api/v1/db/col'

# people = {
#     'item_title': 'person',
#     'additional_lookup': {
#         'url': 'regex("[\w]+")',
#         'field': 'lastname'
#     },
#
#     'schema': {
#         'firstname': {
#             'type': 'string',
#             'minlength': 1,
#             'maxlength': 10,
#         },
#         'lastname': {
#             'type': 'string',
#             'minlength': 1,
#             'maxlength': 15,
#             'required': True,
#             'unique': True,
#         },
#         'role': {
#             'type': 'list',
#             'allowed': ["author", "contributor", "copy"],
#         },
#         'location': {
#             'type': 'dict',
#             'schema': {
#                 'address': {'type': 'string'},
#                 'city': {'type': 'string'}
#             },
#         },
#         'born': {
#             'type': 'datetime',
#         },
#     }
# }
#
# works = {
#     # if 'item_title' is not provided Eve will just strip the final
#     # 's' from resource name, and use it as the item_title.
#     #'item_title': 'work',
#
#     # We choose to override global cache-control directives for this resource.
#     'cache_control': 'max-age=10,must-revalidate',
#     'cache_expires': 10,
#
#     'schema': {
#         'title': {
#             'type': 'string',
#             'required': True,
#         },
#         'description': {
#             'type': 'string',
#         },
#         'owner': {
#             'type': 'objectid',
#             'required': True,
#             # referential integrity constraint: value must exist in the
#             # 'people' collection. Since we aren't declaring a 'field' key,
#             # will default to `people._id` (or, more precisely, to whatever
#             # ID_FIELD value is).
#             'data_relation': {
#                 'resource': 'people',
#                 # make the owner embeddable with ?embedded={"owner":1}
#                 'embeddable': True
#             },
#         },
#     }
# }
#
# # The DOMAIN dict explains which resources will be available and how they will
# # be accessible to the API consumer.
# DOMAIN = {
#     'people': people,
#     'works': works,
# }

DOMAIN = {
}
