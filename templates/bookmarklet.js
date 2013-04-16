(function() {
    var GIST_FILE_PATTERN = /^\/([^\/]+)\/(\d+)$/;
    var REPO_FILE_PATTERN = /^\/([^\/]+)\/([^\/]+)\/tree\/([^\/]+)\/([^\/]+)$/;
    var hostname = document.location.hostname;
    var path     = document.location.pathname;
    var slides   = '{{ request.url_root }}';
    var match    = null;
    
    if (hostname === 'gist.github.com' && (match = path.match(GIST_FILE_PATTERN))) {
        slides = slides + 'gist/' + match[2]; 
    } else if ((hostname === 'www.github.com' || hostname === 'github.com') && (match = path.match(REPO_FILE_PATTERN))) {
        slides = slides + 'repo/' + match[1] + '/' + match[2] + '/' + match[4] + '/?branch=' + match[3]; 
    } else {
        alert('Not a valid remarks slides'); 
    }

    window.open(slides, '_blank','width=600,height=400');
})();
