from flask import session

def clear_session_flashes() -> bool:
    try:
        session['_flashes'].clear()
        return True

    except KeyError:
        return True

    except Exception as e:
        print(e)
        return False