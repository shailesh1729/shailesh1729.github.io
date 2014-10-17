---
layout: default
---
# Test Page

This page is only meant for experimenting with some Markdown syntax. 
Ignore it.



## MathJax samples.

$$a^2 + b^2 = c^2$$

Inline math example: \\( sin(x^2) \\)

$$ \mathsf{Data = PCs} \times \mathsf{Loadings} $$

$$ \mathbf{X}_{n,p} = \mathbf{A}_{n,k} \mathbf{B}_{k,p} $$


## Code Blocks


~~~
def what?
  42
end
~~~
{: .language-ruby}


<pre><code class="javascript">
var s = "JavaScript syntax highlighting";
alert(s);
</code></pre>

<pre><code class="python">
s = "Python syntax highlighting"
print s
</code></pre>


<pre><code class="ruby">
def what?
  42
end 
</code></pre>


<pre><code class="rust">
// Rust
fn main() {

    assert! (Version::parse("1.2.3") == Ok(Version{
        major: 1u,
        minor : 2u,
        patch : 3u,
        pre: vec!(),
        build : vec!(),
    }));

    println!("Versions compared successfully!");
}
</code></pre>
<pre><code class="go">
// Go-lang
package main

import (
    "fmt"
    "os"
    "strings"
)

func main() {
    who := "世界"
    if len(os.Args) > 1 {
        who = strings.Join(os.Args[1:], " ")
    }
    fmt.Println("Hello, ", who)
}
</code></pre>
