#coding=utf-8
import re

#formatProName 函数，将抓取的原始电视节目名字进行处理
def _formatProName(str):
    pattern = re.compile(u"(.+)([(|（])(.+)([)|）])")
    match = pattern.match(str)
    if match:
        #print 1
        return match.group(1)
    pattern = re.compile(u"(《)(.+)(》)")
    match = pattern.match(str)
    if match:
        #print 2
        return match.group(2)
    pattern = re.compile(u"(.+)(《)(.+)(》)")
    match = pattern.match(str)
    if match:
        #print 3
        return match.group(3)
    pattern = re.compile(u"(.+)(\s+)(.+)")
    match = pattern.match(str)
    if match:
        #print 4
        return match.group(1)
    pattern = re.compile(u"(.+)([\[|【])(.+)([\]|】])")
    match = pattern.match(str)
    if match:
        #print 5
        return match.group(1)
    pattern = re.compile(u"(.+)(未删减版|TV版|下部|上部|卫视版|完整版|TVB版)")
    match = pattern.match(str)
    if match:
        #print 6
        return match.group(1)
    return str

#转化为unicode编码，如下调试正则表达式用到
def str2unicode(pName):
    if isinstance(pName, unicode) == False:
        pName = unicode(pName,'utf8')
    else:
        pass
    return pName

def formatProName(str):
    str = _formatProName(str)
    #print str
    pattern = re.compile(u"([^\d]+)(\d+)$")
    match = pattern.match(str)
    if match:
        #print 21
        return match.group(1)
    pattern = re.compile(u"(.+)([\(|（])(.+)([\)|）])")
    match = pattern.match(str)
    if match:
        #print 22
        return match.group(1)
    pattern = re.compile(u"(.+)(第.+[季|部])")
    match = pattern.match(str)
    if match:
        #print 23
        return match.group(1)
    pattern = re.compile(u"(.+)([Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ|Ⅺ]+)")
    match = pattern.match(str)
    if match:
        #print 24
        return match.group(1)
    return str
'''
s = "武媚娘传奇TVB版"
s.strip()
s = str2unicode(s)
s = formatProName(s)
print s
'''
