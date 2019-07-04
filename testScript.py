import sharedfuncs as shared
import sys

def main():

    links = shared.getLinksFromURL("http://localhost:8080/", True)

    for link in links:
        print(link)
        ##sys.stdout.write(link)

    print(len(links))

if __name__ == '__main__':
    main()
