import datetime
import os.path
import osxphotos
import unicodedata

from os import path
from os import listdir
from os.path import isfile, join

class Finding:
    def __init__(self, name, path, isLive, picICloud, picDisk, vidICloud, vidDisk):
        self.name = name
        self.path = path
        self.isLive = isLive
        self.picICloud = picICloud
        self.picDisk = picDisk
        self.vidICloud = vidICloud
        self.vidDisk = vidDisk

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        if self.isLive:
            return self.name + ' in iCloud:' + str(self.picICloud) + ' live:' + str(self.vidICloud) + ' in disk:' + str(self.picDisk) + ' live:' + str(self.vidDisk)
        else:
            return self.name + ' in iCloud:' + str(self.picICloud) + ' in disk:' + str(self.picDisk)

    def isOk(self):
        if self.isLive:
            return self.picICloud and self.picDisk and self.vidICloud and self.vidDisk
        else:
            return self.picICloud and self.picDisk


def main(year):
    diskPhotos = diskPhotoList('/Volumes/2/foto/' + year)
    iCloudPhotos = iCloudPhotoList(year)
    findings = []

    for p in iCloudPhotos:
        album = next(filter(lambda album: album != 'tv', p.albums))

        if year == album[:4]:
            path = '/Volumes/2/foto/' + year + '/' + album + '/' + p.original_filename.lower()
            finding = Finding(
                album + '/' + p.original_filename,
                p.path,
                p.live_photo,
                True,
                path in diskPhotos,
                p.live_photo,
                p.live_photo and (path.replace('.heic', '.mov') in diskPhotos)
            )
            if finding.picDisk:
                diskPhotos.remove(path)
            if finding.vidDisk:
                if path.replace('.heic', '.mov') in diskPhotos:
                    diskPhotos.remove(path.replace('.heic', '.mov'))
                else:
                    if path.replace('.jpg', '.mov') in diskPhotos:
                        diskPhotos.remove(path.replace('.jpg', '.mov'))
                    else:
                        print('consistency error: ' + path.replace('.heic', '.mov'))
            findings.append(finding)
            #print('[path:' + p.path + ']')
        
    for pic in diskPhotos:
        finding = Finding(
                pic[21:],
                pic,
                False,
                False,
                True,
                False,
                pic.replace('.heic', '.mov') in diskPhotos
            )
        if finding.vidDisk:
            diskPhotos.remove(pic.replace('.heic', '.mov'))
        findings.append(finding)

    findings.sort()
    #print(*findings, sep='\n')
    createReport(findings)

def diskPhotoList(albumBasePath):
    diskPhotos = []
    albums = [join(albumBasePath, album) for album in listdir(albumBasePath) if album != '.DS_Store']
    for album in albums:
        albumNormalized = unicodedata.normalize('NFC', album)
        diskPhotos += [join(albumNormalized, unicodedata.normalize('NFC', f.lower())) for f in listdir(album) if f != '.DS_Store']
    return diskPhotos

def iCloudPhotoList(year):
    db = os.path.expanduser("/Volumes/3/iCloud.photoslibrary")
    photosdb = osxphotos.PhotosDB(db)
    return photosdb.photos(
        images = True,
        movies = True,
        from_date = datetime.datetime(int(year), 1, 1),
        to_date = datetime.datetime(int(year), 12, 31),
    )

def createReport(findings):
    f = open('report.html', 'w')
    f.write(open('compare_template.txt', 'r').read())
    for finding in findings:
        if not finding.isOk():
            f.write(''.join(['<tr><td><img src="', finding.path, '" /></td>', 
                '<td>', finding.name, '</td>',
                '<td ', ('class="livephoto"' if finding.isLive else ''), '></td>',
                '<td>', 
                '<span class="icloud ', ('active' if finding.picICloud else 'inactive'), '"></span>',
                (('<span class="livephotovideo active"></span>' if finding.vidICloud else '<span class="livephotovideo inactive"></span>') if finding.isLive else ''),
                '<span class="disk ', ('active' if finding.picDisk else 'inactive'), '"></span>',
                (('<span class="livephotovideo active"></span>' if finding.vidDisk else '<span class="livephotovideo inactive"></span>') if finding.isLive else ''),
                '</td></tr>']))
    f.write('</table></body></html>')
    f.close()

if __name__ == "__main__":
    main('2020')