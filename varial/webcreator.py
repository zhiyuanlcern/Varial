import traceback
import itertools
import datetime
import sys
import os

import toolinterface
import settings
import analysis
import wrappers
import sparseio
import diskio
import util


class WebCreator(toolinterface.Tool):
    """
    Generates webpages for all directories.

    WebCreator instanciates itself recursively for every directory.

    :param name:            str, tool name
    :param working_dir:     str, directory to start with.
    :param no_tool_check:   bool, only run in dirs that ran as a tool before
    :param is_base:         bool, **Do not touch! =)**
    """
    image_postfix = ''

    cross_link_images = {}  # { pathlen: {
                            #         'path/one': {'imagename1', 'imagename2'},
                            #         'path/two': {'imagename1', 'imagename2'},
                            #     }
                            # }

    css_block = """
    body {
      font-family: 'Lucida Grande', 'Helvetica Neue', Helvetica, sans-serif;
      font-size: 9pt;
      background: #fff;
    }
    a {
      color: #666;
    }
    h3 {
      background: darkred;
      color: #fff;
    }
    ul {
      text-align: left;
      display: inline;
      margin: 0;
      padding: 2px 2px 2px 0;
      list-style: none;
    }
    ul li {
      background: #fff;
      color: #888;
      font: 12px/18px sans-serif;
      display: inline-block;
      margin-right: 0px;
      position: relative;
      padding: 0px 2px;
      cursor: pointer;
      -webkit-transition: all 0.2s;
      -moz-transition: all 0.2s;
      -ms-transition: all 0.2s;
      -o-transition: all 0.2s;
      transition: all 0.2s;
    }
    ul li:hover {
      background: #555;
      color: #fff;
    }
    ul li ul {
      padding: 0;
      position: absolute;
      top: 18px;
      left: 0;
      -webkit-box-shadow: none;
      -moz-box-shadow: none;
      box-shadow: none;
      display: none;
      opacity: 0;
      visibility: hidden;
      -webkit-transiton: opacity 0.2s;
      -moz-transition: opacity 0.2s;
      -ms-transition: opacity 0.2s;
      -o-transition: opacity 0.2s;
      -transition: opacity 0.2s;
      -webkit-box-shadow: 0 0 7px rgba(0, 0, 0, 0.35);
      -moz-box-shadow: 0 0 7px rgba(0, 0, 0, 0.35);
      box-shadow: 0 0 7px rgba(0, 0, 0, 0.35);
      z-index: 500;
    }
    ul li ul li {
      background: #fafafa;
      display: block;
    }
    ul li ul li:hover { 
      background: #555;
    }
    ul li ul li:hover a {
      color: #fff;
    }
    ul li:hover ul {
      display: block;
      opacity: 1;
      visibility: visible;
    }
    div.img {
      background: #fff;
      margin-bottom: 35px;
    }
    div.img a {
      color: #888;
      font: 12px/18px sans-serif;
    }
    div.img p {
      margin-top: 3px;
    }
    div.img img {
      margin: 0px;
      margin-right: 7px;
      -webkit-box-shadow: 0 0 7px rgba(0, 0, 0, 0.15);
      -moz-box-shadow: 0 0 7px rgba(0, 0, 0, 0.15);
      box-shadow: 0 0 7px rgba(0, 0, 0, 0.15);
    }
    """

    javascript_block = """
    function ToggleDiv(d) {
      if(document.getElementById(d).style.display == "none") {
        document.getElementById(d).style.display = "block";
      } else {
        document.getElementById(d).style.display = "none";
      }
    }
    """

    rootjs_cont = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN">
    <html lang="en">
       <head>
          <meta http-equiv="X-UA-Compatible" content="IE=Edge">
          <title>Read a ROOT file</title>
          <link rel="shortcut icon" href="img/RootIcon.ico">
          <script
            type="text/javascript"
            src="https://root.cern.ch/js/latest/scripts/JSRootCore.js?gui&mathjax">
          </script>
       </head>
       <body>
          <div id="simpleGUI" path="" files="">
             loading scripts ...
          </div>
       </body>
    </html>
    """
    rootjs_dir_level = 0  # number of directories above wd

    def __init__(self, name=None, working_dir='', no_tool_check=False,
                 is_base=True):
        super(WebCreator, self).__init__(name)
        self.working_dir = working_dir
        self.web_lines = []
        self.subfolders = []
        self.image_names = []
        self.plain_info = []
        self.plain_tex = []
        self.html_files = []
        self.no_tool_check = no_tool_check
        self.is_base = is_base

    def base_configure(self):
        # get image format
        for pf in ['.png', '.jpg', '.jpeg']:
            if pf in settings.rootfile_postfixes:
                self.__class__.image_postfix = pf
                break
        if not self.image_postfix:
            self.message('ERROR No image formats for web available!')
            self.message('ERROR settings.rootfile_postfixes:'
                         + str(settings.rootfile_postfixes))
            self.message('ERROR html production aborted')
            raise RuntimeError('No image postfixes')

        # get base directory
        if not self.working_dir:
            if self.cwd:
                self.working_dir = os.path.join(*self.cwd.split('/')[:-2])
            else:
                self.working_dir = os.path.normpath(analysis.cwd)

        # write rootjs file
        self.__class__.rootjs_dir_level = self.working_dir.count('/')
        with open(os.path.join(self.working_dir, 'rootjs.html'), 'w') as f:
            f.write(self.rootjs_cont)

    def configure(self):
        if self.is_base:
            self.base_configure()

        # collect folders and images
        for wd, dirs, files in os.walk(self.working_dir):
            self.subfolders += list(  # check that tools have worked there..
                d for d in dirs
                if (self.no_tool_check
                    or analysis.lookup_path(os.path.join(self.working_dir, d)))
            )

            # tex files
            res, files = util.project_items(lambda f: f.endswith('.tex'), files)
            self.plain_tex += res

            # websites
            res, files = util.project_items(lambda f: (f.endswith('.html')
                                                        or f.endswith('.htm'))
                                                       and f != 'index.html',
                                       files)
            self.html_files += res

            # plain info
            pf = self.image_postfix
            info, files = util.project_items(
                lambda f: f.endswith('.info'), files)
            res, img_info = util.project_items(
                lambda f: f[:-5] + pf not in files, info)
            self.plain_info += res

            # images
            imgs, files = util.project_items(lambda f: f.endswith(pf), files)
            imgs = map(lambda f: f[:-len(pf)], imgs)  # remove postfixes
            self.image_names += imgs

            break

    def go4subdirs(self):
        for sf in self.subfolders[:]:
            path = os.path.join(self.working_dir, sf)
            inst = self.__class__(self.name, path, self.no_tool_check, False)
            inst.run()
            if not os.path.exists(os.path.join(path, 'index.html')):
                self.subfolders.remove(sf)

    def make_html_head(self):
        self.web_lines += [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<title>',
            self.name + ': ' + self.working_dir,
            '</title>',
            '<style type="text/css">',
            self.css_block,
            '</style>',
            '<script type="text/javascript" language="JavaScript"><!--',
            self.javascript_block,
            '//--></script>',
            '<META name="robots" content="NOINDEX, NOFOLLOW" />',
            '</head>',
            '<body>',
            '<h3>',
            'DISCLAIMER: This page contains an intermediate analysis-snapshot!',
            '</h3>',
        ]

    def make_headline(self):
        breadcrumb = list(d1 for d1 in self.working_dir.split('/') if d1)
        n_folders = len(breadcrumb) - 1
        self.web_lines += (
            '<h2> Folder: ',
            '/'.join('<a href="%sindex.html">%s</a>' % ('../'*(n_folders-i), d)
            for i, d in enumerate(breadcrumb)),
            '</h2>',
            '',
        )

    def make_subfolder_links(self):
        if not self.subfolders:
            return
        self.web_lines += ('<h2>Subfolders:</h2>',)
        for sf in self.subfolders:
            self.web_lines += (
                '<p><a href="%s">%s</a></p>' % (
                    os.path.join(sf, 'index.html'), sf),
            )

    def make_html_file_links(self):
        if not self.html_files:
            return
        self.web_lines += ('<h2>HTML files:</h2>',)
        for hf in self.html_files:
            self.web_lines += (
                '<p><a href="%s">%s</a></p>' % (hf, hf),
            )

    def make_info_file_divs(self):
        if not self.plain_info:
            return
        self.web_lines += ('<h2>Info files:</h2>',)
        for nfo in self.plain_info:
            p_nfo = os.path.join(self.working_dir, nfo)
            try:
                wrp = diskio.read(p_nfo)
                self.web_lines += (
                    '<div>',
                    '<p>',
                    '<b>' + nfo + '</b>',
                    '<p>',
                    '<pre>',
                    str(wrp),
                    '</pre>',
                    '</div>',
                )
            except (SyntaxError, ValueError, IOError):
                self.message('WARNING Could not read info file at %s' % p_nfo)
                etype, evalue, _ = sys.exc_info()
                traceback.print_exception(etype, evalue, None)

    def make_tex_file_divs(self):
        if not self.plain_tex:
            return
        self.web_lines += ('<h2>Tex files:</h2>',)
        for tex in self.plain_tex:
            with open(os.path.join(self.working_dir, tex), 'r') as f:
                self.web_lines += (
                    '<div>',
                    '<p>',
                    '<b>' + tex + '</b>',
                    '<p>',
                    '<pre>',
                )
                self.web_lines += f.readlines()
                self.web_lines += (
                    '</pre>',
                    '</div>',
                )

    def make_image_divs(self):
        if not self.image_names:
            return

        # lin/log pairs
        image_names = sorted(self.image_names)
        image_name_tuples = []
        for i in xrange(len(image_names)):
            try:
                a, b = image_names[i], image_names[i+1]
            except IndexError:
                a, b = image_names[i], ''
            if (a.endswith('_log')
                and image_name_tuples
                and image_name_tuples[-1][1] == a
            ):
                continue
            elif (a.endswith('_lin')
                  and b.endswith('_log')
                  and a[:-4] == b[:-4]
            ):
                image_name_tuples.append((a, b))
            else:
                image_name_tuples.append((a, None))

        # toc
        self.web_lines += (
            '<a name="toc"></a>',
            '<h2>Images:</h2>',
            '<div><p>',
        ) + tuple(
            '<a href="#%s">%s%s</a><br />' % (img, img,
                                            ' (+ log)' if img_log else '')
            for img, img_log in image_name_tuples
        ) + (
            '</p></div>',
        )

        # build rootjs base link (without item yet)
        rootjs_base_link = '../' * (self.working_dir.count('/') 
                                    - self.rootjs_dir_level)
        rootjs_base_link += 'rootjs.html?file='
        rootjs_base_link += os.path.normpath(
            ('../' * self.rootjs_dir_level) +
            os.path.join(self.working_dir, sparseio._rootfile)
        )

        # images
        crosslink_set = set()
        sparse_dict = sparseio.bulk_read_info_dict(self.working_dir)
        for img, img_log in image_name_tuples:

            # try to get from sparseio
            wrp = sparse_dict.get(img[:-4] if img.endswith('_lin') else img)

            # else look for info file on disk
            img_path = os.path.join(self.working_dir, img)
            if (not wrp) and os.path.exists(img_path + '.info'):
                with open(img_path + '.info') as f:
                    wrp = wrappers.Wrapper(**diskio._read_wrapper_info(f))

            if not wrp:
                continue

            rootjs_link = rootjs_base_link + '&item={0}/{0}'.format(wrp.name)
            info_lines = wrp.pretty_writeable_lines()
            history_lines = str(wrp.history)

            i_id = 'info_' + img
            h_id = 'history_' + img
            self.web_lines += (
                '<div class="img">',
                ('<a name="%s"></a>' % img),                    # anchor
                '<!-- CROSSLINK MENU:%s:-->' % img,
                '<p>',                                      # image headline
                ('<b>%s%s</b><br />' % (img, ' (+ _log)' if img_log else '')),
                '<a href="javascript:ToggleDiv(\'' + h_id   # toggle history
                + '\')">(toggle history)</a>',
                '<a href="javascript:ToggleDiv(\'' + i_id   # toggle info
                + '\')">(toggle info)</a>',
                '<a href="%s" target="new">(open in rootjs)</a>' % rootjs_link,
                '<a href="#toc">(back to top)</a>',
                '</p>',
                '<div id="' + h_id                          # history div
                + '" style="display:none;"><pre>',
                history_lines,
                '</pre></div>',
                '<div id="' + i_id                          # info div
                + '" style="display:none;"><pre>',
                info_lines,
                '</pre></div>',
                ('<img src="%s" />' % (img + self.image_postfix)),  # the images
                ('<img src="%s" />' %
                    (img_log + self.image_postfix)) if img_log else '',
                '</div>',
            )

            crosslink_set.add(img)

        # store structured information for cross link menu
        if crosslink_set:
            path = self.working_dir[2:]
            path_depth = path.count('/')
            if not path_depth in self.cross_link_images:
                self.cross_link_images[path_depth] = {}
            self.cross_link_images[path_depth][path] = crosslink_set

    def finalize_page(self):
        self.web_lines += [
            '',
            '<p>Created on '
            + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') +
            ' with '
            '<a href="https://github.com/HeinAtCERN/Varial" target="new">'
            'varial_webcreator'
            '</a>.'
            '</p>',
            '<!-- some empty space (donot block scrolling for a bit) -->',
        ] + list('&nbsp </br>' for _ in xrange(50)) + [
            '</body>',
            '</html>',
        ]

    def write_page(self):
        for i, l in enumerate(self.web_lines):
            self.web_lines[i] += '\n'
        with open(os.path.join(self.working_dir, 'index.html'), 'w') as f:
            f.writelines(self.web_lines)

    def make_cross_link_menus(self):
        def n_path_elements_different(p1, p2):
            return sum(not a == b for a, b in itertools.izip(p1, p2))

        def path_different_at_index(p1, p2):
            return sum(itertools.takewhile(
                int,
                (a == b for a, b in itertools.izip(p1, p2))
            ))

        def rel_path(other_path, nth_elem, img):
            rel_path = '../' * (len(other_path) - nth_elem)
            rel_path += '/'.join(other_path[nth_elem:])
            rel_path += '/index.html#' + img
            return rel_path

        def find_paths_for_image(img, path, paths_with_same_len):
            p = path.split('/')                 # 1st items are current path
            menu_items = list([elem + ' /'] for elem in p)
            for other_path, other_img_set in paths_with_same_len.iteritems():
                if path == other_path:
                    continue
                if img not in other_img_set:
                    continue
                op = other_path.split('/')
                if n_path_elements_different(p, op) != 1:
                    continue

                index = path_different_at_index(p, op)
                menu_items[index].append(
                    '<a href="%s">%s</a>'%(rel_path(op, index, img), op[index])
                )
            return menu_items

        def convert_to_web_line(menu_items):
            def make_submenu(link_list):
                res = '<li>' + link_list[0]
                if len(link_list) > 1:
                    res += '<ul>'
                    for lnk in sorted(link_list[1:]):
                        res += '<li>%s</li>' % lnk
                    res += '</ul>'
                res += '</li>'
                return res

            line = '<div class="crosslinks"><ul>' + ''.join(
                make_submenu(link_list) for link_list in menu_items
            ) + '</ul></div>\n'
            return line

        def write_code_for_page(path, image_menus_items):
            with open(path + '/index.html') as f:
                web_lines = f.readlines()

            for line_no, line in enumerate(web_lines):
                if line.startswith('<!-- CROSSLINK MENU:'):
                    img = line.split(':')[1]
                    web_lines[line_no] = convert_to_web_line(
                                            image_menus_items[img])

            with open(path + '/index.html', 'w') as f:
                f.writelines(web_lines)

        for paths_with_same_len in self.cross_link_images.itervalues():
            for path, img_set in paths_with_same_len.iteritems():
                img_menu_items = {}
                for img in img_set:
                    res = find_paths_for_image(img, path, paths_with_same_len)
                    res.append([img] + list(
                        '<a href="#%s">%s</a>' % (img_, img_)
                        for img_ in img_set)
                    )
                    img_menu_items[img] = res
                write_code_for_page(path, img_menu_items)

    def run(self):
        use_ana_cwd_dsk = diskio.use_analysis_cwd
        use_ana_cwd_spr = sparseio.use_analysis_cwd
        diskio.use_analysis_cwd = False
        sparseio.use_analysis_cwd = False
        self.configure()
        self.go4subdirs()

        if any((self.subfolders,
                self.image_names,
                self.plain_info,
                self.plain_tex,
                self.html_files)):
            self.message('INFO Building page in ' + self.working_dir)
            self.make_html_head()
            self.make_headline()
            self.make_subfolder_links()
            self.make_html_file_links()
            self.make_info_file_divs()
            self.make_tex_file_divs()
            self.make_image_divs()
            self.finalize_page()
            self.write_page()

        if self.is_base:
            self.message('INFO Making cross-link menus.')
            self.make_cross_link_menus()
            diskio.use_analysis_cwd = use_ana_cwd_dsk
            sparseio.use_analysis_cwd = use_ana_cwd_spr
