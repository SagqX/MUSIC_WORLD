# Minimal smoke tests to ensure imports work

def test_imports():
    import config
    from utils.downloader import YouTubeDownloader
    from utils.queue_manager import QueueManager
    from utils.database import Database
    from handlers import music_handlers, user_handlers, admin_handlers

def test_queue_manager():
    from utils.queue_manager import QueueManager
    qm = QueueManager()
    cid = 1
    pos = qm.add_to_queue(cid, {"title": "Test Song", "duration": "03:00", "requested_by": "Tester", "path": "/tmp/a.mp3"})
    assert pos == 1
    assert not qm.is_empty(cid)
    nxt = qm.get_next(cid)
    assert nxt["title"] == "Test Song"
    assert qm.is_empty(cid)
