import re
import markdown
from bs4 import BeautifulSoup


def markdown_add_expandable_images(text):
    """
    Renders Markdown to HTML, and wraps all images in a GLightbox-compatible <a> tag.
    """
    # convert markdown text to HTML and parse img tags
    html = markdown.markdown(text, extensions=['fenced_code'])
    soup = BeautifulSoup(html, 'lxml')
    all_images = soup.find_all('img')

    # loop over images and create and add the <a> tag
    for img in all_images:
        if not img.find_parent('a'):

            # get image source
            img_src = img['src']

            # create <a> tag
            a_tag = soup.new_tag('a', href=img_src)
            a_tag['class'] = 'expandable-image'
            a_tag['data-gallery'] = 'project-gallery'

            # wrap the <img> tag with the <a> tag
            img.wrap(a_tag)

    # return the modified HTML
    return str(soup)

def markdown_parse_figures(text):
    """
    Finds all images within <figure> tags and wraps them for GLightbox,
    using the <figcaption> as the lightbox description.
    """
    html = markdown.markdown(text, extensions=['fenced_code'])
    soup = BeautifulSoup(html, 'lxml')

    # loop over figures and create and add the <a> tag
    for figure in soup.find_all('figure'):
        img = figure.find('img')

        if not img.find_parent('a'):
            figcaption = figure.find('figcaption')

            description_text = ''
            if figcaption:
                description_text = figcaption.get_text(strip=True)

            alt_text = img.get('alt', '')
            img_src = img.get('src', '')

            # create the <a> tag with title and description attributes
            a_tag = soup.new_tag('a', href=img_src, **{
                'class': 'expandable-image',
                'data-gallery': 'project-gallery',
            })

            # wrap the <img> tag with the <a> tag
            img.wrap(a_tag)

    # return the modified HTML
    return str(soup)


def markdown_link_formatting(text:str, class_names:list) -> str:
    """
    Renders Markdown to HTML, and wraps all images in a GLightbox-compatible <a> tag.
    """
    # convert markdown text to HTML and parse a tags
    html = markdown.markdown(text, extensions=['fenced_code'])
    soup = BeautifulSoup(html, 'lxml')
    links_external = soup.find_all('a', href=re.compile(r"^https?://"))

    # loop over images and create and add the custom class
    for link in links_external:
        existing_classes = link.get('class', [])

        for class_name in class_names:
            existing_classes.append(class_name)

        link['class'] = existing_classes

    # return the modified HTML
    return str(soup)
