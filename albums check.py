import os.path

import osxphotos

def main():
    db = os.path.expanduser("/Volumes/3/iCloud.photoslibrary")
    photosdb = osxphotos.PhotosDB(db)
    #print(photosdb.keywords)
    #print(photosdb.persons)
    #print(photosdb.albums)

    #print(photosdb.keywords_as_dict)
    #print(photosdb.persons_as_dict)
    #print(photosdb.albums_as_dict)

    photos = photosdb.photos()
    for p in photos:
        albums = p.albums
        if 'tv' in albums:
            albums.remove('tv')
        if len(albums) > 1:
            print('Picture in multiple albums:')
            print(
                p.uuid,
                p.filename,
                p.original_filename,
                p.date,
                p.description,
                p.title,
                p.keywords,
                p.albums,
                p.persons,
                p.path,
            )
        if len(albums) < 1:
            print('Picture not in albums:')
            print(
                p.uuid,
                p.filename,
                p.original_filename,
                p.date,
                p.description,
                p.title,
                p.keywords,
                p.albums,
                p.persons,
                p.path,
            )

if __name__ == "__main__":
    main()