(function(){
    var d=document,i=new Image,e=encodeURIComponent;
    i.src='%s/a.gif?url='+e(d.location.href)+'&ref='+e(d.referrer)+'&t='+e(d.title);
    })()
