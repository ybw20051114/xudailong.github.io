import os
import io
title='YBW的图床'
def make(s):
    d=os.listdir('.')
    with open('index.html','w') as f:
        
        f.write('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>{0}</title></head><body><h1>{0}</h1><ul>\n'.format(title))
        f.write('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>{0}的索引</title></head><body><h2>{0}的索引</h1><ul>\n'.format(s))
        for i in d:
            if(i!='.git'):
                if(os.path.isdir(i)):
                    os.chdir(i)
                    make(s+i+'/')
                    os.chdir('..')
                    f.write('<li><a href="{0}">{0}/</a></li>\n'.format(i))
                else:
                    f.write('<li><a href="{0}">{0}</a></li>\n'.format(i))
make('http://ybw20051114.github.io/')
print('DONE')