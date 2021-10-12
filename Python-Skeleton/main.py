import time
from smart_m3.m3_kp_api import *

class KP_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        for data in added:
            print(data[2])
            if int(str(data[2])) % 2 != 0:
                kp.load_rdf_remove(data)

if __name__ == '__main__':
    kp = m3_kp_api(PrintDebug=True)

    triples = [
        Triple(URI("sbj1"), URI("rel1"), URI("obj1")),
        Triple(URI("sbj1"), URI("rel2"), URI("obj2")),
        Triple(URI("obj2"), URI("rel1"), Literal("val1")),
    ]
    kp.load_rdf_insert(triples)

    kp.load_query_rdf(Triple(URI("sbj1"), None, None))
    res = kp.result_rdf_query
    print(res)
    kp.load_query_rdf(Triple(None, URI("rel1"), None))
    res = kp.result_rdf_query
    print(res)

    print("\n________UPDATE________\n")

    kp.load_rdf_update([Triple(URI("obj2"), URI("rel1"), Literal("val2"))], [Triple(URI("obj2"), URI("rel1"), Literal("val1"))])
    kp.load_query_rdf(Triple(URI("sbj1"), None, None))
    res = kp.result_rdf_query
    print(res)
    kp.load_query_rdf(Triple(None, URI("rel1"), None))
    res = kp.result_rdf_query
    print(res)

    print("\n________REMOVE________\n")

    kp.load_rdf_remove(Triple(URI("obj2"), None, None))
    kp.load_query_rdf(Triple(URI("sbj1"), None, None))
    res = kp.result_rdf_query
    print(res)
    kp.load_query_rdf(Triple(None, URI("rel1"), None))
    res = kp.result_rdf_query
    print(res)

    subscription_triple = Triple(URI("Agent_X"), URI("has_item"), None)
    handler = KP_Handler(kp)
    handler_subscription = kp.load_subscribe_RDF(subscription_triple, handler)

    for i in range(3):
        kp.load_rdf_insert([Triple(URI("Agent_X"), URI("has_item"), Literal(i)), Triple(URI("Agent_X"), URI("has_item"), Literal(i+1))])
        time.sleep(3)

    time.sleep(3)

    kp.load_unsubscribe(handler_subscription)

    kp.clean_sib()
    kp.leave()