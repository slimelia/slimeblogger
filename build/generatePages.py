#!/usr/bin/env python3

import os
import markdown
import pystache
import bs4
import blogpostParser

def getBlogpostsFromDir(dirOfPosts):
	blogParser = blogpostParser.blogpostParser()
	blogpostList = []
	
	
	for filename in os.listdir(dirOfPosts):
		blogpostDict = {}
		fileHandler = open('{0}/{1}'.format(dirOfPosts,filename),'r',encoding='utf-8')
		lineToParse = fileHandler.readline()
		blogpostDict["body"] = markdown.markdown(fileHandler.read())
		fileHandler.close()
		
		blogpostAttributes = blogParser.splitBlogStringToDict(lineToParse)
		blogpostAttributes["title"] = blogpostAttributes["title"].lower()
		blogpostDict.update(blogpostAttributes)
		
		blogpostList.append(blogpostDict)
	
	return blogpostList
	
def generateBlogContent(blogpostTemplateLocation,blogpostList):
	posts = []
	content = {}
	
	fileHandler = open(blogpostTemplateLocation,"r")
	blogpostTemplate = fileHandler.read()
	fileHandler.close()
	
	for blogpost in blogpostList:
		generatedBlogPost = pystache.render(blogpostTemplate,blogpost)
		posts.append({"post":generatedBlogPost})
	
	content["content"] = posts
	return content

def generateSite(siteTemplateLocation,content):
	fileHandler = open(siteTemplateLocation,"r")
	siteTemplate = fileHandler.read()
	fileHandler.close()
	
	generatedSite = pystache.render(siteTemplate,content)
	
	return generatedSite
	
if __name__ == "__main__":
	postDir = "posts"
	postTemplate = "templates/blogpost.mustache"
	siteTemplate = "templates/site.mustache"
	
	postList = getBlogpostsFromDir(postDir)
	content = generateBlogContent(postTemplate,postList)
	siteHtml = generateSite(siteTemplate,content)
	
	parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')
	
	index_html = open('../public_html/index.html',"w")
	index_html.write(parsedSiteHtml.prettify())
	index_html.close()
	
	
	
	
