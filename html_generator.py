with open("Top200.txt") as file:
    data = file.readlines()

def fill_template(html_code,output_file):
    # Read in the file
    with open('template.html', 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('####REPLACE####',html_code)

    # Write the file out again
    with open(output_file, 'w') as file:
        file.write(filedata)

def gen_thumbnail(domain):
    with open(f"./headers/{domain}.txt") as f:
        headers=f.read().replace("\n","</br>\n")
    return (f'''
<div class="thumb-box" onclick="toggle('{domain}')">
    <span class="master_container">
        <img src="./images/{domain}.png" alt="">
        <span class="overlay-box">
            <span class="main-title">{domain}</span>
            <span class="description">
            <p>


            <button type="button" class="btn btn-primary">Primary</button>
            <button type="button" class="btn btn-secondary">Secondary</button>
            <button type="button" class="btn btn-success">Success</button>
             </p>
            </span>
        </span>
    </span>
</div>''')


def grid_it(data, col=3):
    thumbnails=[]
    temp_thumbnails=[]
    for i in range(0,len(data)):
        if i % col == 0 and i!=0:
            thumbnails.append(temp_thumbnails)
            temp_thumbnails=[]
            temp_thumbnails.append(gen_thumbnail(data[i].rstrip()))
        else:
            temp_thumbnails.append(gen_thumbnail(data[i].rstrip()))
    if temp_thumbnails:
        thumbnails.append(temp_thumbnails)
    return thumbnails



import jinja2
import os

x=grid_it(data)


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=False)
JINJA_ENVIRONMENT.globals['STATIC_PREFIX'] = './static/'
template = JINJA_ENVIRONMENT.get_template('./static/base.html')
with open("./index.html","w") as f:
    f.write(template.render(thumbnails=x))