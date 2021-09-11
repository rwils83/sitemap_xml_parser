import xml.dom.minidom as md
import requests as rq
import time
import os
import argparse
import sys


class SitemapParser:
    def __init__(self, sitemapurl, outfile, verbosity=None, delete=False, output=False, exclude=None):
        if "http" not in sitemapurl:
            sitemapurl = f"https://{sitemapurl}"
        self.start_time = time.time()
        if output:
            print(f"[+] Constructing new Parser at {time.ctime(self.start_time)}, this may take a few minutes.")
        else:
            print(f"[+] Constructing new Parser at {time.ctime(self.start_time)}, this may take a few minutes. "
                  f"A URL count will be displayed, but no URLs will be saved. Use -o to save URLs to a file")
        self.sitemaps = []
        self.exclude = exclude
        self.files = []
        self.urls = []
        self.outfile = outfile
        self.robots = sitemapurl
        self.delete = delete
        self.verbosity = verbosity
        print(self.verbosity)
        self.output = output
        self.__get_sitemap_urls()
        self.__get_sitemap()
        self.__get_urls()
        if self.output:
            self._write_urls()
        if self.delete is not False:
            self._delete_local_files()
        self._count_urls()

    def __get_sitemap_urls(self):
        print(f'[+] Getting urls for sitemaps from {self.robots}')
        r = rq.get(self.robots)
        for line in r.text.split('\n'):
            if "sitemap" in line:
                if line.split(" ")[-1] not in self.sitemaps and line.split(" ")[-1] != self.exclude:
                    self.sitemaps.append(line.split(' ')[-1])
        if len(self.sitemaps) > 0:
            print("[+] Finished. Starting next step")
        else:
            print("[-] No sitemaps found")
            sys.exit()

    def __get_sitemap(self):
        print(f"[+] Getting files from {len(self.sitemaps)} URLs and writing locally at ./sitemaps/")
        for sitemap in self.sitemaps:
            if self.verbosity:
                print(f"[+] Getting sitemap @ {sitemap}")
            if sitemap.split('/')[-1] not in self.files:
                self.files.append(sitemap.split('/')[-1])
            r = rq.get(sitemap)
            if not os.path.exists("./sitemaps"):
                os.makedirs("./sitemaps")
            with open(f"./sitemaps/{sitemap.split('/')[-1]}", "w+") as f:
                f.write(r.text)
        print("[+] Finished. Starting next step")

    def __get_urls(self):
        print(f"[+] Parsing for URLs in {len(self.files)} Files")
        for file in self.files:
            if self.verbosity is not None:
                print(f"[+] Parsing ./sitemaps/{file}for urls")
            xml_file = f'./sitemaps/{file}'
            DOMTree = md.parse(xml_file)
            root_node = DOMTree.documentElement
            loc_nodes = root_node.getElementsByTagName("loc")
            for loc in loc_nodes:
                if loc.childNodes[0].data not in self.urls:
                    self.urls.append(loc.childNodes[0].data)
            return self.urls

    def _delete_local_files(self):
        print(f'[-] Deleting locally saved xml files')
        for file in self.files:
            if self.verbosity:
                print(f'Removing ./sitemap/{file}')
            os.remove(f'./sitemaps/{file}')
        os.rmdir("./sitemaps")

    def _write_urls(self):
        print(f'[+] Writing URLs to {self.outfile}')
        with open(f'{self.outfile}', "w+") as f:
            for url in self.urls:
                f.write(url+"\n")

    def _count_urls(self):
        if not self.delete:
            if time.time() - self.start_time < 60:
                print(f'[+] Parser found {len(self.urls)} URLs within {len(self.files)} files in {round((time.time() - self.start_time))} seconds.')
            else:
                print(f'[+] Parser found {len(self.urls)} URLs within {len(self.files)} files in {round((time.time() - self.start_time))/60} minutes.')
        else:
            if time.time() - self.start_time < 60:
                print(f'[+] Parser found {len(self.urls)} URLs within {len(self.files)} files in {round((time.time() - self.start_time))} seconds. {len(self.files)} files deleted from local storage')
            else:
                print(f'[+] Parser found {len(self.urls)} URLs within {len(self.files)} files in {round((time.time() - self.start_time))/60} minutes. {len(self.files)} files deleted from local storage')


def parse_args():
    description = "Parse Sitemap.xml files."
    parser = argparse.ArgumentParser(description=description)
    requirednamed = parser.add_argument_group('Required Arguments')
    requirednamed.add_argument('-u',
                               '--url',
                               action="store",
                               help="Enter the URL that lists sitemap.xml files, ex. https://www.tiktok.com/robots.txt",
                               required=True)
    parser.add_argument('-o',
                        '--output',
                        action="store",
                        nargs="?",
                        const="all_urls.txt",
                        help="Use -o/--output to write all URLs found to a file")
    parser.add_argument('-d',
                        '--delete',
                        action="store_true",
                        help="Use -d/--delete to delete all locally written xml files")
    parser.add_argument('-f',
                        '--file',
                        action='store',
                        nargs='?',
                        const="all_urls.txt",
                        help="Future use")
    parser.add_argument('-dl',
                        '--delete_url_file',
                        action="store",
                        nargs='?',
                        const="all_urls.txt",
                        help="Use to clean up a url file from previous runs, "
                             "mostly was used during testing the script.")
    parser.add_argument('-v', '--verbose', action="store_true", help="Use for debugging")
    parser.add_argument('-e', '--exclude', action="store", nargs="?", const=None, help="Use to exclude urls breaking the script")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    if args.delete_url_file:
        os.remove(f'{args.delete_url_file}')
    else:
        if args.output:
            new_parser = SitemapParser(args.url, delete=args.delete, output=True, outfile=args.output, verbosity=args.verbose, exclude=args.exclude)
        else:
            new_parser = SitemapParser(args.url, outfile=args.output, delete=args.delete, output=False, verbosity=args.verbose, exclude=args.exclude)
