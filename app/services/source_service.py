def build_sources(results):
        sources = []

        for item in results:

                filename = item.get("metadata",{}).get("filename","Unknown").source.append(filename)

        return list(set(sources))