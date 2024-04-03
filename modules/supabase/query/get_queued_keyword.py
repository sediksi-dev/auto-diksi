from modules.supabase.db import db


def get_queued():
    query = (
        "id: id",
        "keyword: keywords",
        "language: language",
        "mode: rewrite_mode",
        "date: rewrite_date",
        "status: status",
    )
    try:
        response = db.table("seed_keywords").select(*query)
        response = response.eq("status", "queue")
        response = response.limit(1)
        response = response.order("rewrite_date", desc=False)
        response = response.maybe_single()
        response = response.execute()

        return response.data

    except Exception as e:
        print("Error getting seed keywords by date: ", e)
        return str(e)
