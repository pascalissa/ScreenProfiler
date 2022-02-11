import argparse
import asyncio
from pyppeteer import launch
from datetime import datetime
from os import mkdir

sizes = {"small":[1024,768], "medium":[1280,1024], "large":[1600,1200]}

def create_folder_structure(project_name):
    mkdir(f"./{project_name}")
    mkdir(f"./{project_name}/images")
    mkdir(f"./{project_name}/headers")
    mkdir(f"./{project_name}/html")

def __url2filename__(url):
    x = url.rstrip().rstrip("/").split("/")[-1:][0]
    if "%3F" in x:
        if x.split("%3F")[0] != "":
            return x.split("%3F")[0]
        else:
            return x.split("%3F")[1]
    elif "?" in x:
        if x.split("?")[0] != "":
            return x.split("?")[0]
        else:
            return x.split("?")[1]
    elif "#" in x:
        if x.split("#")[0] != "":
            return x.split("#")[0]
        else:
            return x.split("#")[1]
    else:
        return x

async def get_url(browser, url, viewport_width, viewport_height):
    # open a new page, I still dont know how to control the default page opened
    page = await browser.newPage()
    # set resolution of browser view port
    await page.setViewport({'width': viewport_width, 'height': viewport_height})
    # go to url and wait for page to load
    try:
        page_response=await page.goto(url, {'waitUntil' : 'networkidle2'})
        if page_response:
            with open(f"./{args.project_name}/headers/{__url2filename__(url)}.header.txt","w") as header_file:
                for key in page_response.headers:
                    header_file.writelines(f"{key} : {page_response.headers[key]}\n")
            page_body = await page_response.text()
            with open(f"./{args.project_name}/html/{__url2filename__(url)}.html","w") as html_file:
                for line in page_body:
                    html_file.writelines(line)
            #wait for the assertion to show up or Duo times out
            await page.screenshot({"path":f"./{args.project_name}/images/{__url2filename__(url)}.png"})
            await page.close()
    except:
        print(f"{url} could not be resolved or accessed")


async def safe_get_url(tabs,browser,url,viewport_width, viewport_height):
    async with tabs:  # semaphore limits num of simultaneous downloads
        return await get_url(browser,url,viewport_width, viewport_height)


async def browse_urls(threads, urls, viewport_width, viewport_height, show_browser, ignore_ssl_errors):
    tabs = asyncio.Semaphore(threads)  #semaphore limits num of simultaneous tabs
    # Launch a browser either visible or not, and ignore errors or not
    browser = await launch({'headless': not(show_browser), 'ignoreHTTPSErrors':ignore_ssl_errors})
    tasks = [
        asyncio.ensure_future(safe_get_url(tabs,browser,url,viewport_width, viewport_height))  # creating task starts coroutine
        for url in urls
    ]
    await asyncio.gather(*tasks)  # await moment all downloads done




parser = argparse.ArgumentParser(prog='Screen Profiler')
parser.add_argument('URLfile', type=str,
                    help='A file containing the list of urls you want to profile, each full url on a seperate line.')
parser.add_argument('-p', '--project-name', dest='project_name', action='store', type=str, default="",
                    help="Project name will be the folder name created, and all data is stored under.")
parser.add_argument('-t', '--tabs', dest='tabs', action='store', type=int, default=10,
                    help="The number of tabs you want the web browser to open.")
parser.add_argument('-s', '--size', dest='size', action='store', nargs=2, default=[1280,1024],
                    help="The size of the screenshot in terms of width and height, default is [1280, 1024]")
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help="Render verbose output, including redirects and program errors.")
parser.add_argument('-i', '--ignore-tls-errors', dest='ignore_tls', action='store_true',
                    help="Don't verify SSL/TLS certificates.")
parser.add_argument('-b', '--browser', dest='browser', action='store_true',
                    help="Show browser while operations are on going.")

args = parser.parse_args()


if args.project_name=="":
    now = datetime.now()
    args.project_name = now.strftime("%Y-%m-%d-%H-%M-%S")

width=int(args.size[0])
height=int(args.size[1])

with open(args.URLfile) as f:
    urls=f.readlines()

create_folder_structure(args.project_name)
asyncio.get_event_loop().run_until_complete(browse_urls(threads=args.tabs, urls=urls, viewport_width=width,
                                                       viewport_height=height, show_browser=args.browser, ignore_ssl_errors=args.ignore_tls))