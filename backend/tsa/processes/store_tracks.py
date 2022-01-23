from tsa.storage import WriteStorageMethod


def store_tracks(tracking_generator, storage: WriteStorageMethod):
    for next_frame_data in tracking_generator:
        storage.save_frame(*next_frame_data)

    storage.close()
