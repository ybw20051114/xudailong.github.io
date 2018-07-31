# -*- coding: utf-8 -*-
import codecs
import sys
 
 
import tomd
 
 
reload(sys)
sys.setdefaultencoding('utf8')  # 设置默认编码格式为'utf-8'
 
 
save_file='D:\markdown.md'
 
 
def run():
    html = getHtml()
    print html
    mdTxt = tomd.Tomd(html).markdown
    print 'markdown :{}'.format(mdTxt)
    createFile(mdTxt)
 
 
def createFile(mdTxt):
    print '系统默认编码：{}'.format(sys.getdefaultencoding())
    print '准备写入文件：{}'.format(save_file)
    #r+ 打开一个文件用于读写。文件指针将会放在文件的开头。
    #w+ 打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    #a+ 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
    f = codecs.open(save_file,'w+','utf-8')
    # f.write('###{}\n'.format(url))
    f.write(mdTxt)
    #f.write(mdTxt)
    f.close()
    print '写入文件结束：{}'.format(f.name)
 
 
 
 
def getHtml():
    return u'''<div id="article-content" class="hola-content">
<p>我们想象一下自来水厂到你家的水管网是一个复杂的有向图，每一节水管都有一个最大承载流量。自来水厂不放水，你家就断水了。但是就算自来水厂拼命的往管网里面注水，你家收到的水流量也是上限（毕竟每根水管承载量有限）。你想知道你能够拿到多少水，这就是一种网络流问题。</p>
<p>在网上找了很久资料，虽然讲解网络流的资料很多但是浅显易懂的很少<del>（可能是我太蒻了吧）</del>，写这篇文章只希望点进来的人都能学会网络流<del>（都能点赞）</del></p>
<p>我尽量用通俗易懂的语言讲解，同时结合图示理解。</p>
<p>我将讲解以下网络流算法：</p>
<ol>
<li>
<p>最大流</p>
</li>
<li>
<p>最小费用最大流</p>
</li>
</ol>
<h2>先从最基础的最大流开始：</h2>
<p>何为最大流问题？</p>
<p>简单来说就是水流从一个源点s通过很多路径，经过很多点，到达汇点t，问你最多能有多少水能够到达t点。</p>
<p>结合图示理解：
<img src="https://cdn.luogu.org/upload/pic/24602.png" alt=""></p>
<p>从s到t经过若干个点，若干条边，每一条边的水流都不能超过边权值（可以小于等于但不能大于），所以该图的最大流就是10+22+45=77。</p>
<p>如果你还是不能理解，我们就换一种说法，假设s城有inf个人想去t城，但是从s到t要经过一些城市才能到达，（以上图为例）其中s到3城的火车票还剩10张，3到t的火车票还剩15张，其他路以此类推，问最终最多能有多少人能到达t城？<del>（假设这个地区只有火车，没有汽车飞机，步行和骑自行车会累死就不考虑了，再假设所有人都买得起火车票。）</del></p>
<p>那怎么么解决这个问题呢？</p>
<p>对于这个问题，刚看到时，你有什么想法？</p>
<p>或许你会有一个这样的思路：从s开始找所有能到达t的路径，然后找每条路径上权值最小的边（或者说能承受水流最小的管子），再进行其它操作，就能找到这张图的最大流。</p>
<p>然后我们有</p>
<h2>EK（Edmond—Karp）算法。</h2>
<h6>其实还有其它算法，但由于过于复杂<del>（作者太懒不想画图）</del>，（以作者的语文水平）很难讲的通俗易懂，就不献丑了。</h6>
<p>这里我就不介绍那么多公式定理之类的了<del>（为了通俗易懂，并且不把你绕晕）</del>，为方便讲解，引入一个概念：</p>
<h2>增广路：</h2>
<p>增广路是指从s到t的一条路，流过这条路，使得当前的流（可以到达t的人）可以增加。</p>
<h4>那么求最大流问题可以转换为不断求解增广路的问题，并且，显然当图中不存在增广路时就达到了最大流。</h4>
<p>具体怎么操作呢？</p>
<p>其实很简单，直接从s到t广搜即可，从s开始不断向外广搜，通过权值大于0的边（因为后面会减边权值，所以可能存在边权为0的边），直到找到t为止，然后找到该路径上边权最小的边，记为mi，然后最大流加mi，然后把该路径上的每一条边的边权减去mi，直到找不到一条增广路（从s到t的一条路径）为止。（为什么要用mi呢？你要争取在这条路上多走更多人，但又不能让人停在某个城市）</p>
<p>具体操作：</p>
<p>找增广路：</p>
<pre><code class="hljs cpp"><span class="hljs-function"><span class="hljs-keyword">bool</span> <span class="hljs-title">bfs</span><span class="hljs-params">()</span></span>{
    <span class="hljs-built_in">queue</span>&lt;<span class="hljs-keyword">int</span>&gt;q;
    <span class="hljs-built_in">memset</span>(inque,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(inque));
    <span class="hljs-built_in">memset</span>(pre,<span class="hljs-number">-1</span>,<span class="hljs-keyword">sizeof</span>(pre));
    inque[s]=<span class="hljs-number">1</span>;
    q.push(s);
    <span class="hljs-keyword">while</span>(!q.empty()){
        <span class="hljs-keyword">int</span> u=q.front();
        q.pop();
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=head[u];i;i=node[i].next){
            <span class="hljs-keyword">int</span> d=node[i].v;
            <span class="hljs-keyword">if</span>(!inque[d]&amp;&amp;node[i].val){<span class="hljs-comment">//node[i].val==0则已经该路径满了</span>
            inque[d]=<span class="hljs-number">1</span>;
            pre[d].v=u;
            pre[d].edge=i;
            <span class="hljs-keyword">if</span>(d==t)<span class="hljs-keyword">return</span> <span class="hljs-number">1</span>;
            q.push(d);
            }
        }
    }
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}<span class="hljs-comment">//是否有增广路 </span></code></pre>
<p>那个pre数组是由来记录路径的，它长这样：</p>
<pre><code class="hljs cpp"><span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">Pre</span>{</span>
    <span class="hljs-keyword">int</span> v;<span class="hljs-comment">//该点的前一个点（从起点过来） </span>
    <span class="hljs-keyword">int</span> edge;<span class="hljs-comment">//与该点相连的边（靠近起点的） </span>
}pre[<span class="hljs-number">101010</span>];</code></pre>
<p>然后直接累加最大流（注意加的时候要把改边边权减去相应的流量，防止一直重复加同一段流）</p>
<p>那代码是长这样的吗?</p>
<pre><code class="hljs cpp"><span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">EK</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> ans=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">while</span>(bfs()){
        <span class="hljs-keyword">int</span> mi=inf;
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=t;i!=s;i=pre[i].v){
        mi=min(mi,node[pre[i].edge].val);
        }
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=t;i!=s;i=pre[i].v){
        node[pre[i].edge].val-=mi;
        }
        ans+=mi;
    }
    <span class="hljs-keyword">return</span> ans;
}</code></pre>
<p>当然不是，万一第一次流错了使得这样的流法无法得到最大流怎么办？
还是以刚才那张图为例，为了防止你再翻上去，我直接再放一次：
<img src="https://cdn.luogu.org/upload/pic/24602.png" alt=""></p>
<p>如果你第一次的增广路是：s-&gt;3-&gt;5-&gt;t流量显然是10，第二次的增广路是s-&gt;4-&gt;5-&gt;t流量显然是35（因为5-&gt;t的流量有10点被3号点来的人占领了)。</p>
<p>而这种方案显然不如：s-&gt;4-&gt;5-&gt;t流量为45，s-&gt;3-&gt;t流量为10。</p>
<p>那程序怎么知道哪种方案最优？</p>
<p>它当然不知道，我们要把所有情况都找一遍，难道要回溯？</p>
<p>当然不，这里使用一种高级技巧，加反向边。什么意思？</p>
<p>以下图为例：
<img src="https://cdn.luogu.org/upload/pic/24603.png" alt=""></p>
<p>这是刚才那张图，我们在每条边都加了一条反向的，权值为0的边（红色的边）。</p>
<p>有什么用呢？</p>
<p>占空间？拖时间？显然不是。</p>
<p>先不管有什么用，加了反向边，我们再跑一次EK，这次，除了要给增广路上的边都减去该路上的最小流量以外，还要给反向边加上最小流量。为什么？先别管。</p>
<p>先找增广路，比如说我们走了s-&gt;3-&gt;5-&gt;t，那么图会变成：</p>
<p><img src="https://cdn.luogu.org/upload/pic/24604.png" alt=""></p>
<p>再找一次增广路，这次比如说我们走s-&gt;4-&gt;5-&gt;t。
<img src="https://cdn.luogu.org/upload/pic/24605.png" alt=""></p>
<p>（那个65被洛谷打了<del>美观的</del>水印，将就看吧）</p>
<p>再找一次增广路，这次我们找s-&gt;4-&gt;5-&gt;3-&gt;t
<img src="https://cdn.luogu.org/upload/pic/24606.png" alt=""></p>
<p>好像有点奇怪。你可能会想：为什么这次搜索的时候走了反向边（红色）的边，为什么走了反向边（红色）的边会加正向边（黑色）的边？</p>
<p>这就好像是45个人沿着s-&gt;4-&gt;5-&gt;t的路线想去t城，到了5城却发现有10个来自3城的人先定了5-&gt;t的票！他们十分焦急，总不能让他们在5城等吧。</p>
<p>怎么办呢？他们通过反向边上的标记发现了那10个人是来自3城的，利用标记，他们发现那10个人可以直接从3城到t城，于是他们<del>（利用了哆啦A梦的时光机）</del>告诉还在3城时的那10个人可以直接走3-&gt;t这条路，然后他们就可以买到空出来的5-&gt;t的10张票了。</p>
<h4>现在你知道反向边的作用了吧：留下一个标记，让后面的人有机会让前面的人走另一条路。</h4>
<p>理解了反向边的作用，恭喜你已经理解了EK求解最大流算法的原理了。</p>
<p>下面讲解关于反向边在代码中的实现：</p>
<p>关于反向边在加正向边时要一起加上，边权为0，然后在寻找增广路时就没必要关注一条边是正向边还是反向边了，在统计最大流时，要把每一条经过的边的边权减去这条增广路的流（最小流量），每条经过的边的反向边（反向边的反向边是正向边，负负得正）加上这条增广路的流。</p>
<h4>现在还有一个小问题，怎么通过一条边的编号求它的反向边的编号。</h4>
<p>由于正向边和反向边是一起加的，所以反向边的编号与正向边的编号只相差1。</p>
<p>那就好办了。</p>
<p>如果第一条边的编号是偶数，就有</p>
<p>正向边的编号^1==反向边的编号；反向边的编号^1==正向边的编号。（？为什么？）</p>
<p>那么接下来就来证明：当正向边的编号为2<em>n时反向边的编号为2</em>n+1。设n的二进制表示为XXXXX，则2n==n&lt;&lt;1 因此2n的二进制表示:XXXXX0,而2*n+1的二进制表示：XXXXX1。
那肯定（2n）^1==2n+1;(2n+1）^1==2n。</p>
<p>都讲完了，那就附上完整代码：</p>
<pre><code class="hljs cpp"><span class="hljs-comment">//EK算法求解最大流 </span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;iostream&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstring&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstdio&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;algorithm&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;queue&gt;</span></span>
<span class="hljs-keyword">using</span> <span class="hljs-keyword">namespace</span> <span class="hljs-built_in">std</span>;
<span class="hljs-keyword">const</span> <span class="hljs-keyword">int</span> inf=<span class="hljs-number">1</span>&lt;&lt;<span class="hljs-number">30</span>;
<span class="hljs-keyword">int</span> n,m,s,t;
<span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">Node</span>{</span>
    <span class="hljs-keyword">int</span> v;
    <span class="hljs-keyword">int</span> val;
    <span class="hljs-keyword">int</span> next;
}node[<span class="hljs-number">201010</span>];
<span class="hljs-keyword">int</span> top=<span class="hljs-number">1</span>,head[<span class="hljs-number">101010</span>];<span class="hljs-comment">//top必须从一个奇数开始，一般用-1但我不习惯，解释见下方 </span>
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">void</span> <span class="hljs-title">addedge</span><span class="hljs-params">(<span class="hljs-keyword">int</span> u,<span class="hljs-keyword">int</span> v,<span class="hljs-keyword">int</span> val)</span></span>{
    node[++top].v=v;
    node[top].val=val;
    node[top].next=head[u];
    head[u]=top;
}
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">int</span> <span class="hljs-title">Read</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> x=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">char</span> c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;<span class="hljs-string">'9'</span>||c&lt;<span class="hljs-string">'0'</span>)c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;=<span class="hljs-string">'0'</span>&amp;&amp;c&lt;=<span class="hljs-string">'9'</span>)x=x*<span class="hljs-number">10</span>+c-<span class="hljs-string">'0'</span>,c=getchar();
    <span class="hljs-keyword">return</span> x;
}
<span class="hljs-keyword">int</span> inque[<span class="hljs-number">101010</span>];<span class="hljs-comment">//点是访问过里 </span>
<span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">Pre</span>{</span>
    <span class="hljs-keyword">int</span> v;<span class="hljs-comment">//该点的前一个点（从起点过来） </span>
    <span class="hljs-keyword">int</span> edge;<span class="hljs-comment">//与该点相连的边（靠近起点的） </span>
}pre[<span class="hljs-number">101010</span>];
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">bool</span> <span class="hljs-title">bfs</span><span class="hljs-params">()</span></span>{
    <span class="hljs-built_in">queue</span>&lt;<span class="hljs-keyword">int</span>&gt;q;
    <span class="hljs-built_in">memset</span>(inque,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(inque));
    <span class="hljs-built_in">memset</span>(pre,<span class="hljs-number">-1</span>,<span class="hljs-keyword">sizeof</span>(pre));
    inque[s]=<span class="hljs-number">1</span>;
    q.push(s);
    <span class="hljs-keyword">while</span>(!q.empty()){
        <span class="hljs-keyword">int</span> u=q.front();
        q.pop();
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=head[u];i;i=node[i].next){
            <span class="hljs-keyword">int</span> d=node[i].v;
            <span class="hljs-keyword">if</span>(!inque[d]&amp;&amp;node[i].val){<span class="hljs-comment">//node[i].val==0则已经该路径满了 </span>
            pre[d].v=u;
            pre[d].edge=i;
            <span class="hljs-keyword">if</span>(d==t)<span class="hljs-keyword">return</span> <span class="hljs-number">1</span>;
            inque[d]=<span class="hljs-number">1</span>;
            q.push(d);
            }
        }
    }
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}<span class="hljs-comment">//是否有增广路 </span>
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">EK</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> ans=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">while</span>(bfs()){
        <span class="hljs-keyword">int</span> mi=inf;
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=t;i!=s;i=pre[i].v){
            mi=min(mi,node[pre[i].edge].val);<span class="hljs-comment">//每次只能增加增广路上最小的边的权值 </span>
        }
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=t;i!=s;i=pre[i].v){
            node[pre[i].edge].val-=mi;
            node[pre[i].edge^<span class="hljs-number">1</span>].val+=mi;
            <span class="hljs-comment">//反向的边的编号是正向边的编号^1</span>
            <span class="hljs-comment">//这就是为什么top开始时必须是奇数 </span>
        }
        ans+=mi;
    }
    <span class="hljs-keyword">return</span> ans;
}
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">main</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i;
    n=Read(),m=Read(),s=Read(),t=Read();
    <span class="hljs-keyword">int</span> u,v,w;
    <span class="hljs-keyword">for</span>(i=<span class="hljs-number">1</span>;i&lt;=m;i++)
    u=Read(),v=Read(),w=Read(),addedge(u,v,w),addedge(v,u,<span class="hljs-number">0</span>);
    <span class="hljs-built_in">printf</span>(<span class="hljs-string">"%d"</span>,EK());
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}</code></pre>
<p>题目是：<a href="https://www.luogu.org/problemnew/show/P3376#sub">P3376 【模板】网络最大流</a></p>
<p><del>还有一道模版题<a href="https://www.luogu.org/problemnew/show/P2740"> P2740 [USACO4.2]草地排水Drainage Ditches</a>（水双倍经验）</del></p>
<p>那么这个<del>（乱七八糟的）</del>算法有什么用呢？</p>
<h3>经典应用：二分图匹配。</h3>
<p>什么意思？</p>
<p>给两个集合：A，B，其中A有一些元素a1,a2,a3……，B有一些元素b1,b2,b3……</p>
<p>其中a1想和b1，b4，……中的一个配对，a2想和b1，b250，b2500……<del>（这些数字没什么特别含义）</del>配对，为最优情况下能有多少组配对成功。</p>
<p>二分匹配模板题：
<a href="https://www.luogu.org/problemnew/show/P2756#sub">P2756 飞行员配对方案问题</a></p>
<p>怎么做呢？</p>
<p>其实二分匹配问题可以转换为网络流问题。</p>
<p>把集合A当成起点，集合B当成终点，若集合一中元素a可以对应集合二中元素b，则加一条a指向b流量为一的边 </p>
<p>新增加两个点，s和t，s有指向所有起点的边，所有终点有指向t的边，只需计算s到t的最大流，用EK算法即可。</p>
<p>本题要求记录配对方案，只需在找增广路时加个标记即可。</p>
<p>附上代码：</p>
<pre><code class="hljs cpp"><span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;iostream&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstring&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstdio&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;algorithm&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;queue&gt;</span></span>
<span class="hljs-keyword">using</span> <span class="hljs-keyword">namespace</span> <span class="hljs-built_in">std</span>;
<span class="hljs-keyword">int</span> n,m;
<span class="hljs-keyword">const</span> <span class="hljs-keyword">int</span> mx=<span class="hljs-number">1</span>&lt;&lt;<span class="hljs-number">30</span>;
<span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">Node</span>{</span>
    <span class="hljs-keyword">int</span> v;
    <span class="hljs-keyword">int</span> val;
    <span class="hljs-keyword">int</span> nxt;
}node[<span class="hljs-number">5010</span>];
<span class="hljs-keyword">int</span> top=<span class="hljs-number">1</span>;
<span class="hljs-keyword">int</span> s=<span class="hljs-number">1008</span>,t=<span class="hljs-number">1009</span>;
<span class="hljs-keyword">int</span> ansk[<span class="hljs-number">1050</span>];<span class="hljs-comment">//标号为i的外籍飞行员和标号为ansk[i]-n的英国飞行员对应 </span>
<span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">P</span>{</span>
    <span class="hljs-keyword">int</span> fa;
    <span class="hljs-keyword">int</span> edge;
}pre[<span class="hljs-number">1010</span>];<span class="hljs-comment">//在一条增广路中，节点的前一个节点和与之相连的边 </span>
<span class="hljs-keyword">int</span> head[<span class="hljs-number">1010</span>];
<span class="hljs-keyword">int</span> inque[<span class="hljs-number">1010</span>];
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">int</span> <span class="hljs-title">Read</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> x=<span class="hljs-number">0</span>,f=<span class="hljs-number">1</span>;
    <span class="hljs-keyword">char</span> c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;<span class="hljs-string">'9'</span>||c&lt;<span class="hljs-string">'0'</span>){
        <span class="hljs-keyword">if</span>(c==<span class="hljs-string">'-'</span>)f=<span class="hljs-number">-1</span>;
        c=getchar();
    }
    <span class="hljs-keyword">while</span>(c&gt;=<span class="hljs-string">'0'</span>&amp;&amp;c&lt;=<span class="hljs-string">'9'</span>)x=x*<span class="hljs-number">10</span>+c-<span class="hljs-string">'0'</span>,c=getchar();
    <span class="hljs-keyword">return</span> x*f;
}
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">void</span> <span class="hljs-title">addedge</span><span class="hljs-params">(<span class="hljs-keyword">int</span> u,<span class="hljs-keyword">int</span> v,<span class="hljs-keyword">int</span> val)</span></span>{
    node[++top].v=v;
    node[top].val=val;
    node[top].nxt=head[u];
    head[u]=top;
}
<span class="hljs-function"><span class="hljs-keyword">bool</span> <span class="hljs-title">addroad</span><span class="hljs-params">()</span></span>{
    <span class="hljs-built_in">memset</span>(pre,<span class="hljs-number">-1</span>,<span class="hljs-keyword">sizeof</span>(pre));
    <span class="hljs-built_in">memset</span>(inque,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(inque));
    <span class="hljs-built_in">queue</span>&lt;<span class="hljs-keyword">int</span>&gt;q;
    q.push(s);
    inque[s]=<span class="hljs-number">1</span>;
    <span class="hljs-keyword">while</span>(!q.empty()){
        <span class="hljs-keyword">int</span> u=q.front();
        q.pop();
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=head[u];i;i=node[i].nxt){
            <span class="hljs-keyword">int</span> d=node[i].v;
            <span class="hljs-keyword">int</span> val=node[i].val;
            <span class="hljs-keyword">if</span>(val!=<span class="hljs-number">0</span>&amp;&amp;inque[d]==<span class="hljs-number">0</span>){
                pre[d].fa=u;
                pre[d].edge=i;
                <span class="hljs-keyword">if</span>(d==t)<span class="hljs-keyword">return</span> <span class="hljs-number">1</span>;
                q.push(d);
                inque[d]=<span class="hljs-number">1</span>;
            }
        }
    }
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}<span class="hljs-comment">//寻找增广路 </span>
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">EK</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> ans=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">while</span>(addroad()){
        <span class="hljs-keyword">int</span> mi=mx;
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=t;i!=s;i=pre[i].fa)mi=min(mi,node[pre[i].edge].val);
        <span class="hljs-keyword">for</span>(<span class="hljs-keyword">int</span> i=t;i!=s;i=pre[i].fa)ansk[pre[i].fa]=i,node[pre[i].edge].val-=mi,node[pre[i].edge^<span class="hljs-number">1</span>].val+=mi;
        ans+=mi;
    }
    <span class="hljs-keyword">return</span> ans;
}<span class="hljs-comment">//EK求最大流</span>
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">main</span><span class="hljs-params">()</span></span>{
    m=Read(),n=Read();
    <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i;
    <span class="hljs-comment">//英国飞行员用n+i号点表示，外籍飞行员用i号点表示 </span>
    <span class="hljs-keyword">for</span>(i=<span class="hljs-number">1</span>;i&lt;=n;i++)addedge(i+n,t,<span class="hljs-number">1</span>),addedge(t,i+n,<span class="hljs-number">0</span>);<span class="hljs-comment">//使所有英国空军和汇点相连 </span>
    <span class="hljs-keyword">for</span>(i=<span class="hljs-number">1</span>;i&lt;=m;i++)addedge(s,i,<span class="hljs-number">1</span>),addedge(i,s,<span class="hljs-number">0</span>);<span class="hljs-comment">//使所有外籍空军和源点相连</span>
    <span class="hljs-keyword">int</span> u,v;
    <span class="hljs-keyword">while</span>(<span class="hljs-number">1</span>){
    u=Read(),v=Read();
    <span class="hljs-keyword">if</span>(u==<span class="hljs-number">-1</span>&amp;&amp;v==<span class="hljs-number">-1</span>)<span class="hljs-keyword">break</span>;
    addedge(u,v+n,<span class="hljs-number">1</span>);
    addedge(v+n,u,<span class="hljs-number">0</span>);
    } 
    <span class="hljs-built_in">printf</span>(<span class="hljs-string">"%d\n"</span>,EK());
    <span class="hljs-keyword">for</span>(i=<span class="hljs-number">1</span>;i&lt;=n;i++)<span class="hljs-keyword">if</span>(ansk[i]!=<span class="hljs-number">0</span>)<span class="hljs-built_in">printf</span>(<span class="hljs-string">"%d %d\n"</span>,i,ansk[i]-n);
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}</code></pre>
<p>其实相比于网络流，二分匹配还有更快的方法，匈牙利算法，这里就不详细讲解了，今天的重点是网络流。</p>
<p>对于这道题，网络流会超时，匈牙利算法不会超时：
<a href="https://www.luogu.org/problemnew/show/P3386#sub">P3386 【模板】二分图匹配</a></p>
<p>感兴趣的可以自行研究，还是给出代码吧：</p>
<pre><code class="hljs cpp"><span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;iostream&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstring&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;algorithm&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstdio&gt;</span></span>
<span class="hljs-keyword">using</span> <span class="hljs-keyword">namespace</span> <span class="hljs-built_in">std</span>;
<span class="hljs-keyword">int</span> n,m,e;
<span class="hljs-keyword">int</span> to[<span class="hljs-number">1010</span>][<span class="hljs-number">1010</span>];
<span class="hljs-keyword">int</span> used[<span class="hljs-number">1010</span>],y[<span class="hljs-number">1010</span>];<span class="hljs-comment">//m集合中的点是否使用过，若使用过，与它匹配的是谁 </span>
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">int</span> <span class="hljs-title">Read</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> x=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">char</span> c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;<span class="hljs-string">'9'</span>||c&lt;<span class="hljs-string">'0'</span>)c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;=<span class="hljs-string">'0'</span>&amp;&amp;c&lt;=<span class="hljs-string">'9'</span>)x=x*<span class="hljs-number">10</span>+c-<span class="hljs-string">'0'</span>,c=getchar();
    <span class="hljs-keyword">return</span> x;
}
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">find</span><span class="hljs-params">(<span class="hljs-keyword">int</span> x)</span></span>{
    <span class="hljs-keyword">for</span>(<span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i=<span class="hljs-number">1</span>;i&lt;=m;i++){
        <span class="hljs-keyword">if</span>(to[x][i]==<span class="hljs-number">1</span>&amp;&amp;used[i]==<span class="hljs-number">0</span>){
            used[i]=<span class="hljs-number">1</span>;
            <span class="hljs-keyword">if</span>(y[i]==<span class="hljs-number">0</span>||find(y[i])==<span class="hljs-number">1</span>){
                y[i]=x;
            <span class="hljs-keyword">return</span> <span class="hljs-number">1</span>;
            }
     }
    }
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">findans</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> ans=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">for</span>(<span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i=<span class="hljs-number">1</span>;i&lt;=n;i++){
        <span class="hljs-built_in">memset</span>(used,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(used));
        ans+=find(i);
    }
    <span class="hljs-keyword">return</span> ans;
}
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">main</span><span class="hljs-params">()</span></span>{
    n=Read(),m=Read(),e=Read();
    <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i;
    <span class="hljs-keyword">int</span> u,v;
    <span class="hljs-keyword">for</span>(i=<span class="hljs-number">1</span>;i&lt;=e;i++){
        u=Read(),v=Read();
        <span class="hljs-keyword">if</span>(u&gt;n)<span class="hljs-keyword">continue</span>;
        <span class="hljs-keyword">if</span>(v&gt;m)<span class="hljs-keyword">continue</span>;
        to[u][v]=<span class="hljs-number">1</span>;
    }
    <span class="hljs-built_in">printf</span>(<span class="hljs-string">"%d"</span>,findans());
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}</code></pre>
<h2>然后就是最小费用最大流了</h2>
<p>听名字就和上面讲的差不多。</p>
<p>什么是最小费用最大流呢？</p>
<p>以下图为例
<img src="https://cdn.luogu.org/upload/pic/24738.png" alt=""></p>
<p>上图中没打（）的为边权（最大流量），打（）的为单位流量的价格</p>
<p>还是用刚才那种通俗易懂的解释方法</p>
<p>假设s城有inf个（穷）人想去t城，但是从s到t要经过一些城市才能到达，其中s到3城的火车票还剩10张票价为6元/人，3到t的火车票还剩15张票价为7元/人，其他路以此类推，问最终最多能有多少人能到达t城？</p>
<p>（由于是穷人）他们希望能在最多人到达t城的同时花最少的钱，问最少的钱是多少？</p>
<p>有了刚才学习最大流的基础，相信接下来的讲解应该很容易看懂。</p>
<p>还是找增广路的思想，但是这次我们找花费最小（即s到t费用最小）的增广路。</p>
<p>怎么实现呢？</p>
<p>看到那个（即s到t费用最小）了吗？</p>
<p>想到了什么？</p>
<p>最短路算法！</p>
<p>也就是说我们在找增广路时，把bfs换成spfa就可以了！</p>
<p>附上代码（相信看到这里，不用看我打的代码你都能自己打出来了）：</p>
<pre><code class="hljs cpp"><span class="hljs-function"><span class="hljs-keyword">bool</span> <span class="hljs-title">spfa</span><span class="hljs-params">()</span></span>{
    <span class="hljs-built_in">memset</span>(pre,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(pre));
    <span class="hljs-built_in">memset</span>(dist,<span class="hljs-number">0x3f</span>,<span class="hljs-keyword">sizeof</span>(dist));
    <span class="hljs-built_in">memset</span>(inque,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(inque));
    <span class="hljs-built_in">queue</span>&lt;<span class="hljs-keyword">int</span>&gt;q;
    q.push(s);
    inque[s]=<span class="hljs-number">1</span>;
    dist[s]=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">while</span>(!q.empty()){
        <span class="hljs-keyword">int</span> u=q.front();
        inque[u]=<span class="hljs-number">0</span>;
        q.pop();
        <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i,d,w;
        <span class="hljs-keyword">for</span>(i=head[u];i;i=node[i].next){
            d=node[i].v;
            w=node[i].w;
            <span class="hljs-keyword">if</span>(node[i].val&amp;&amp;dist[d]&gt;dist[u]+w){
            <span class="hljs-comment">//这里dist表示从s到某个点d的单位最小费用</span>
                dist[d]=dist[u]+w;
                pre[d].fa=u;
                pre[d].adge=i;
                <span class="hljs-keyword">if</span>(inque[d]==<span class="hljs-number">0</span>){
                    q.push(d);
                    inque[d]=<span class="hljs-number">1</span>;
                }
            }
        }
    }
    <span class="hljs-keyword">return</span> dist[t]!=<span class="hljs-number">0x3f3f3f3f</span>;
}<span class="hljs-comment">//寻找费用最小的增广路</span></code></pre>
<p>还有一点要注意：反向边的花费为正向边的相反数。</p>
<p>？</p>
<p>其实很好理解，如果那几个人不走这条路，那么这条路的钱就不用花了，但是因为刚才（前面走过的增广路）走过时花了钱，这次走反向边要退钱。</p>
<p>然后就是计算最大流和对应的最小费用了</p>
<pre><code class="hljs cpp"><span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">EK</span><span class="hljs-params">()</span></span>{<span class="hljs-comment">//最小费用最大流的EK算法</span>
    maxflow=<span class="hljs-number">0</span>;
    cost=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">int</span> mi;
    <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i;
    <span class="hljs-keyword">while</span>(spfa()){
        mi=inf;
        <span class="hljs-keyword">for</span>(i=t;i!=s;i=pre[i].fa)mi=min(mi,node[pre[i].adge].val);
        <span class="hljs-keyword">for</span>(i=t;i!=s;i=pre[i].fa){
            node[pre[i].adge].val-=mi;
            node[pre[i].adge^<span class="hljs-number">1</span>].val+=mi;
        }
        maxflow+=mi;
        cost+=mi*dist[t];
        <span class="hljs-comment">//本增广路最多能流的流量*从s到t的单位费用</span>
    }
    <span class="hljs-keyword">return</span> maxflow;
}</code></pre>
<p>这道题是<a href="https://www.luogu.org/problemnew/show/P3381#sub">P3381 【模板】最小费用最大流</a></p>
<p>附上完整代码：</p>
<pre><code class="hljs cpp"><span class="hljs-comment">//EK算法求解最小费用最大流</span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;iostream&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstring&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;algorithm&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;cstdio&gt;</span></span>
<span class="hljs-meta">#<span class="hljs-meta-keyword">include</span><span class="hljs-meta-string">&lt;queue&gt;</span></span>
<span class="hljs-keyword">using</span> <span class="hljs-keyword">namespace</span> <span class="hljs-built_in">std</span>;
<span class="hljs-keyword">int</span> maxflow;<span class="hljs-comment">//最大流</span>
<span class="hljs-keyword">int</span> cost;<span class="hljs-comment">//最小费用 </span>
<span class="hljs-keyword">int</span> top=<span class="hljs-number">1</span>,head[<span class="hljs-number">5010</span>];
<span class="hljs-keyword">const</span> <span class="hljs-keyword">int</span> inf=<span class="hljs-number">1</span>&lt;&lt;<span class="hljs-number">30</span>;
<span class="hljs-keyword">int</span> dist[<span class="hljs-number">5010</span>];
<span class="hljs-keyword">int</span> inque[<span class="hljs-number">5010</span>];
<span class="hljs-keyword">int</span> n,m,s,t;
<span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">Node</span>{</span>
    <span class="hljs-keyword">int</span> v;
    <span class="hljs-keyword">int</span> w;<span class="hljs-comment">//该边单位流量的费用</span>
    <span class="hljs-keyword">int</span> next;
    <span class="hljs-keyword">int</span> val;<span class="hljs-comment">//该边最大流量 </span>
}node[<span class="hljs-number">101100</span>];
<span class="hljs-class"><span class="hljs-keyword">struct</span> <span class="hljs-title">P</span>{</span>
    <span class="hljs-keyword">int</span> fa;<span class="hljs-comment">//增广路上该点的父亲 </span>
    <span class="hljs-keyword">int</span> adge;<span class="hljs-comment">//该点与父亲相连的边的编号 </span>
}pre[<span class="hljs-number">5010</span>];
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">int</span> <span class="hljs-title">Read</span><span class="hljs-params">()</span></span>{
    <span class="hljs-keyword">int</span> x=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">char</span> c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;<span class="hljs-string">'9'</span>||c&lt;<span class="hljs-string">'0'</span>)c=getchar();
    <span class="hljs-keyword">while</span>(c&gt;=<span class="hljs-string">'0'</span>&amp;&amp;c&lt;=<span class="hljs-string">'9'</span>)x=x*<span class="hljs-number">10</span>+c-<span class="hljs-string">'0'</span>,c=getchar();
    <span class="hljs-keyword">return</span> x;
}
<span class="hljs-function"><span class="hljs-keyword">inline</span> <span class="hljs-keyword">void</span> <span class="hljs-title">addedge</span><span class="hljs-params">(<span class="hljs-keyword">int</span> u,<span class="hljs-keyword">int</span> v,<span class="hljs-keyword">int</span> val,<span class="hljs-keyword">int</span> w)</span></span>{
    node[++top].v=v;
    node[top].val=val;
    node[top].w=w;
    node[top].next=head[u];
    head[u]=top;
}
<span class="hljs-function"><span class="hljs-keyword">bool</span> <span class="hljs-title">spfa</span><span class="hljs-params">()</span></span>{
    <span class="hljs-built_in">memset</span>(pre,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(pre));
    <span class="hljs-built_in">memset</span>(dist,<span class="hljs-number">0x3f</span>,<span class="hljs-keyword">sizeof</span>(dist));
    <span class="hljs-built_in">memset</span>(inque,<span class="hljs-number">0</span>,<span class="hljs-keyword">sizeof</span>(inque));
    <span class="hljs-built_in">queue</span>&lt;<span class="hljs-keyword">int</span>&gt;q;
    q.push(s);
    inque[s]=<span class="hljs-number">1</span>;
    dist[s]=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">while</span>(!q.empty()){
        <span class="hljs-keyword">int</span> u=q.front();
        inque[u]=<span class="hljs-number">0</span>;
        q.pop();
        <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i,d,w;
        <span class="hljs-keyword">for</span>(i=head[u];i;i=node[i].next){
            d=node[i].v;
            w=node[i].w;
            <span class="hljs-keyword">if</span>(node[i].val&gt;<span class="hljs-number">0</span>&amp;&amp;dist[d]&gt;dist[u]+w){
                dist[d]=dist[u]+w;
                pre[d].fa=u;
                pre[d].adge=i;
                <span class="hljs-keyword">if</span>(inque[d]==<span class="hljs-number">0</span>){
                    q.push(d);
                    inque[d]=<span class="hljs-number">1</span>;
                }
            }
        }
    }
    <span class="hljs-keyword">return</span> dist[t]!=<span class="hljs-number">0x3f3f3f3f</span>;
}<span class="hljs-comment">//寻找费用最小的增广路</span>
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">EK</span><span class="hljs-params">()</span></span>{<span class="hljs-comment">//最小费用最大流的EK算法</span>
    maxflow=<span class="hljs-number">0</span>;
    cost=<span class="hljs-number">0</span>;
    <span class="hljs-keyword">int</span> mi;
    <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i;
    <span class="hljs-keyword">while</span>(spfa()){
        mi=inf;
        <span class="hljs-keyword">for</span>(i=t;i!=s;i=pre[i].fa)mi=min(mi,node[pre[i].adge].val);
        <span class="hljs-keyword">for</span>(i=t;i!=s;i=pre[i].fa){
            node[pre[i].adge].val-=mi;
            node[pre[i].adge^<span class="hljs-number">1</span>].val+=mi;
        }
        maxflow+=mi;
        cost+=mi*dist[t];
    }
    <span class="hljs-keyword">return</span> maxflow;
}
<span class="hljs-function"><span class="hljs-keyword">int</span> <span class="hljs-title">main</span><span class="hljs-params">()</span></span>{
    n=Read(),m=Read(),s=Read(),t=Read();
    <span class="hljs-keyword">register</span> <span class="hljs-keyword">int</span> i;
    <span class="hljs-keyword">int</span> u,v,val,w;
    <span class="hljs-keyword">for</span>(i=<span class="hljs-number">1</span>;i&lt;=m;i++){
        u=Read(),v=Read(),val=Read(),w=Read();
        addedge(u,v,val,w);
        addedge(v,u,<span class="hljs-number">0</span>,-w);
    }
    <span class="hljs-built_in">printf</span>(<span class="hljs-string">"%d "</span>,EK());
    <span class="hljs-built_in">printf</span>(<span class="hljs-string">"%d"</span>,cost);
    <span class="hljs-keyword">return</span> <span class="hljs-number">0</span>;
}</code></pre>
<p>另外，最小费用最大流还有更高效的zkw算法，由于有点复杂<del>（作者太懒）</del>就不讲解的，感兴趣的自行百度。</p>
<p>好像有人想让我讲一下Dinic，可以看一下<a href="https://www.luogu.org/blog/ONE-PIECE/wang-lao-liu-jiang-xie-zhi-dinic">网络最大流Dinic讲解</a></p>
<h1>求赞</h1>
</div>
    '''
    
run()