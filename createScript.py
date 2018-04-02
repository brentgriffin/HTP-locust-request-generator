import sharedfuncs as shared
import sys
import threading
import time

threadLock = threading.Lock()
visitedLinks = set()
linksToVisit = set()

sys.stderr.write('Developed and tested with python3.6.2\n')
if len(sys.argv) != 3:
    sys.stderr.write('ERROR - must have exactly 2 parameters based in.  These required parameters are:\n')
    sys.stderr.write('\tURLPrefix, numberOfThreadsToUse(integer value required)\n')
    sys.stderr.write('\n\tExample:\n')
    sys.stderr.write('\t\t' + str(sys.argv[0]) + ' http://localhost:8080 5\n')
    exit(1)

homepageURL = str(sys.argv[1])
threadCount = int(sys.argv[2])
linksToVisit.add('/')

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        sys.stderr.write("Starting " + self.name + '\r\n')

        threadLock.acquire()
        try:
            linkToVisit = linksToVisit.pop()
            visitedLinks.add(linkToVisit)
        except KeyError:
            linkToVisit = ''
        threadLock.release()

        while linkToVisit:
            links = []
            if shared.canHaveAdditionalLinks(linkToVisit):
                sys.stderr.write(self.name + '|Visiting URL: ' + homepageURL + linkToVisit + '\r\n')

                links = shared.getLinksFromURL(homepageURL + linkToVisit, True)

            threadLock.acquire()
            for link in links:
                if link not in visitedLinks:
                    linksToVisit.add(link)
            try:
                linkToVisit = linksToVisit.pop()
                visitedLinks.add(linkToVisit)
            except KeyError:
                linkToVisit = ''
            threadLock.release()
        
        sys.stderr.write("Stopping " + self.name + '\r\n')


def main():
    threads = []

    for i in range(1, threadCount):
        threads.append(myThread(i, 'Thread-' + str(i)))

    for t in threads:
        t.start()
        time.sleep(2)

    for t in threads:
        t.join()

    shared.printLocustRequestFile(sorted(visitedLinks))


if __name__ == '__main__':
    main()
