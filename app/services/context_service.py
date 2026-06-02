def build_context(documents):
        context = ""

        for doc in documents:

                context += (
                        doc.page_content
                        + "\n\n"
                )
        return context