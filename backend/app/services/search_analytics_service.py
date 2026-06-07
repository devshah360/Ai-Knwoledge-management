from app.models.search_model import SearchHistory

def save_search(db,query):
        search = SearchHistory(query=query)

        db.add(search)
        db.commit()
        