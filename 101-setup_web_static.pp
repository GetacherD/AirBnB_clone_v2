# configure new Server

package { 'nginx':
  ensure => 'installed',
}
$conf = "server {
	listen   80 default_server;
	listen   [::]:80 default_server;
	root     /var/www/html;
	index    index.html index.htm;
	location /redirect_me {
		return 301 https://www.youtube.com;
	}
	location /hbnb_static {
		alias /data/web_static/current;
		index index.html;
	}
	error_page 404 /custom_404.html;
	location = /custom_404.html {
		root /var/www/errors/;
		internal;
	}
		
}
"
file {'/data/web_static/releases/':
  enusre => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file {'/data/web_static/shared/':
  enusre => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file {'/data/web_static/releases/test/':
  enusre => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  target => '/data/web_static/releases/test/'
}

file {'/data/web_static/current':
  enusre => 'link',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}
file {'/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $conf
}

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => 'Hello World!'
}

file { '/var/www/errors/custom_404.html':
  ensure  => 'present',
  content => "Ceci n\'est pas une page"
}

service {'nginx':
  ensure  => running,
  require => Package['nginx']
}
