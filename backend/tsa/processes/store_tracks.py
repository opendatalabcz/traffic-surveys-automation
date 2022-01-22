from tsa.storage import StorageMethod


def store_tracks(tracking_generator, storage: StorageMethod):
    for next_frame_data in tracking_generator:
        storage.save_frame(*next_frame_data)

    storage.close()
