import os
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Download static files from CDN'

    def handle(self, *args, **kwargs):
        # Criar diretórios se não existirem
        static_dir = os.path.join('core', 'static')
        css_dir = os.path.join(static_dir, 'css')
        js_dir = os.path.join(static_dir, 'js')
        webfonts_dir = os.path.join(static_dir, 'webfonts')
        
        for directory in [static_dir, css_dir, js_dir, webfonts_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # URLs dos arquivos
        files = {
            os.path.join(css_dir, 'bootstrap.min.css'): 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
            os.path.join(css_dir, 'all.min.css'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
            os.path.join(js_dir, 'bootstrap.bundle.min.js'): 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
            # Font Awesome Webfonts
            os.path.join(webfonts_dir, 'fa-solid-900.woff2'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.woff2',
            os.path.join(webfonts_dir, 'fa-solid-900.ttf'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-solid-900.ttf',
            os.path.join(webfonts_dir, 'fa-regular-400.woff2'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-regular-400.woff2',
            os.path.join(webfonts_dir, 'fa-regular-400.ttf'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-regular-400.ttf',
            os.path.join(webfonts_dir, 'fa-brands-400.woff2'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-brands-400.woff2',
            os.path.join(webfonts_dir, 'fa-brands-400.ttf'): 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/webfonts/fa-brands-400.ttf',
        }

        # Download dos arquivos
        for file_path, url in files.items():
            self.stdout.write(f'Baixando {url}...')
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                self.stdout.write(self.style.SUCCESS(f'Arquivo salvo em {file_path}'))
            else:
                self.stdout.write(self.style.ERROR(f'Erro ao baixar {url}'))
