from boa3.builtin import metadata, NeoMetadata


def Main() -> int:
    return 5


@metadata
def email_manifest() -> NeoMetadata:
    meta = NeoMetadata()
    meta.email = 'test@test.com'
    return meta