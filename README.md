<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta name="generator" content="pandoc" />
  <meta name="author" content="Thibault BRONCHAIN &lt;thibault@mc2.io&gt;" />
  <meta name="author" content="Ken CHEN &lt;ken@mc2.io&gt;" />
  <meta name="author" content="Michael CHO &lt;michael@mc2.io&gt;" />
  <link rel="stylesheet" href="README.css" type="text/css" />
</head>
<body>
<div id="header">
<h1 class="title">Pysa</h1>
<h2 class="author">Thibault BRONCHAIN &lt;<script type="text/javascript">
                   <!--
                   h='&#x6d;&#x63;&#50;&#46;&#x69;&#x6f;';a='&#64;';n='&#116;&#104;&#x69;&#98;&#x61;&#x75;&#108;&#116;';e=n+a+h;
                   document.write('<a h'+'ref'+'="ma'+'ilto'+':'+e+'">'+e+'<\/'+'a'+'>');
                   // -->
                   </script><noscript>&#116;&#104;&#x69;&#98;&#x61;&#x75;&#108;&#116;&#32;&#x61;&#116;&#32;&#x6d;&#x63;&#50;&#32;&#100;&#x6f;&#116;&#32;&#x69;&#x6f;</noscript>&gt;</h2>
<h2 class="author">Ken CHEN &lt;<script type="text/javascript">
                   <!--
                   h='&#x6d;&#x63;&#50;&#46;&#x69;&#x6f;';a='&#64;';n='&#x6b;&#x65;&#110;';e=n+a+h;
                   document.write('<a h'+'ref'+'="ma'+'ilto'+':'+e+'">'+e+'<\/'+'a'+'>');
                   // -->
                   </script><noscript>&#x6b;&#x65;&#110;&#32;&#x61;&#116;&#32;&#x6d;&#x63;&#50;&#32;&#100;&#x6f;&#116;&#32;&#x69;&#x6f;</noscript>&gt;</h2>
<h2 class="author">Michael CHO &lt;<script type="text/javascript">
                   <!--
                   h='&#x6d;&#x63;&#50;&#46;&#x69;&#x6f;';a='&#64;';n='&#x6d;&#x69;&#x63;&#104;&#x61;&#x65;&#108;';e=n+a+h;
                   document.write('<a h'+'ref'+'="ma'+'ilto'+':'+e+'">'+e+'<\/'+'a'+'>');
                   // -->
                   </script><noscript>&#x6d;&#x69;&#x63;&#104;&#x61;&#x65;&#108;&#32;&#x61;&#116;&#32;&#x6d;&#x63;&#50;&#32;&#100;&#x6f;&#116;&#32;&#x69;&#x6f;</noscript>&gt;</h2>
<h3 class="date">Date: 2013-07-23 (Wed, 24 Jul 2013)</h3>
</div>
<div id="TOC">
<ul>
<li><a>NAME</a></li>
<li><a>SYNOPSIS</a></li>
<li><a>DESCRIPTION</a></li>
<li><a>OPTIONS</a><ul>
<li><a>Options list</a><ul>
<li><a>-h, –help</a></li>
<li><a>-q, –quiet</a></li>
<li><a>-p, –puppet</a></li>
<li><a>-s, –salt</a></li>
<li><a>-m module-name, –module module-name</a></li>
<li><a>-c config-file-path, –config config-file-path</a></li>
<li><a>-o output-path, –output output-path</a></li>
<li><a>-f filter-config-path, –filter filter-config-path</a></li>
</ul></li>
</ul></li>
<li><a>REPLICATION</a></li>
<li><a>RESOURCES</a><ul>
<li><a>configuration files - file</a></li>
<li><a>packages - package</a></li>
<li><a>services - service</a></li>
<li><a>hosts - host</a></li>
<li><a>users - user</a></li>
<li><a>groups - group</a></li>
<li><a>mounts - mount</a></li>
<li><a>crons - cron</a></li>
<li><a>ssh keys - key</a></li>
<li><a>sources repositories - source</a></li>
<li><a>package managers repositories - repository</a></li>
</ul></li>
<li><a>AUTOCONF TOOLS MODULES</a><ul>
<li><a>Puppet modules</a></li>
</ul></li>
<li><a>FILTERS</a><ul>
<li><a>common action keys</a><ul>
<li><a>_contentrefer</a></li>
</ul></li>
<li><a>addition section</a><ul>
<li><a>addition section description</a></li>
<li><a>addition section format</a></li>
<li><a>addition section action keys</a></li>
</ul></li>
<li><a>discard section</a><ul>
<li><a>discard section description</a></li>
<li><a>discard section format</a></li>
<li><a>discard section action keys</a></li>
</ul></li>
<li><a>replace section</a><ul>
<li><a>replace section description</a></li>
<li><a>replace section format</a></li>
<li><a>replace section action keys</a></li>
</ul></li>
<li><a>update section</a><ul>
<li><a>update section description</a></li>
<li><a>update section format</a></li>
<li><a>update section action keys</a></li>
</ul></li>
</ul></li>
<li><a>USAGE EXAMPLES</a></li>
<li><a>NOTES</a></li>
<li><a>BUGS</a></li>
</ul>
</div>
<dl>
<dt>Info</dt>
<dd><p>Reverse Engineer Server Configurations</p>
</dd>
<dt>Organisation</dt>
<dd><ol start="3" style="list-style-type: lower-alpha">
<li>2013 - MADEIRACLOUD LTD.</li>
</ol>
</dd>
<dt>Revision</dt>
<dd><p>v0.2.5a</p>
</dd>
<dt>Description</dt>
<dd><p>Pysa scans your system and reverse engineers its configurations for easy replication.</p>
</dd>
</dl>
<h1>NAME</h1>
<p>pysa - Reverse Engineer Server Configurations</p>
<h1>SYNOPSIS</h1>
<p><strong>pysa</strong> [ <strong>-hqps</strong> ] [ <strong>-m</strong> <em>module-name</em> ] [ <strong>-o</strong> <em>output-path</em> ] [<strong>-c</strong> <em>config-file-path</em>] [ <strong>-f</strong> <em>filter-config-path</em> ]</p>
<h1>DESCRIPTION</h1>
<p><strong>pysa</strong> scans your system and reverse engineers its configurations for easy replication.</p>
<p><strong>pysa</strong> is able to scan your system, looking for different resources to deploy and generates some “autoconf” tools script to deploy it later on another computer.</p>
<p>See RESOURCES_ section for complete list of managed resources.</p>
<p><strong>pysa</strong> is able to generates the configuration in Puppet (see <a href="http://docs.puppetlabs.com/references/latest/type.html">Puppet</a> documentation) or SaltStack (see <a href="http://salt.readthedocs.org/en/latest/contents.html">SaltStack</a> documentation) format.</p>
<h1>OPTIONS</h1>
<h2>Options list</h2>
<h3>-h, –help</h3>
<p>Display the short help.</p>
<h3>-q, –quiet</h3>
<p>Activate quiet mode and displays only error messages. By default, <strong>pysa</strong> displays all log messages.</p>
<h3>-p, –puppet</h3>
<p>Generates Puppet output.</p>
<h3>-s, –salt</h3>
<p>Generates SaltStack output.</p>
<h3>-m module-name, –module module-name</h3>
<p>Choose output module name. Default value: <em>pysa</em></p>
<h3>-c config-file-path, –config config-file-path</h3>
<p>Specify a configuration file. See examples file for more details <em>pysa.cfg</em></p>
<h3>-o output-path, –output output-path</h3>
<p>Choose the output filter for generated scripts. Default value: <em>output</em></p>
<h3>-f filter-config-path, –filter filter-config-path</h3>
<p>Specify a filter configuration file. See FILTERS_ section for more details.</p>
<h1>REPLICATION</h1>
<p><strong>pysa</strong> generates a puppet module containing several configuration scripts.</p>
<p>There are two ways to use <strong>pysa</strong> ’s output:</p>
<ul>
<li>You can manually configure the configuration manager and add <strong>pysa</strong> ’s module to it</li>
<li>If you’re using Puppet module, you can use the <em>pysa2puppet</em> script to deploy a complete and standalone setup. The script is interactive and will ask you all necessaries info (see usage first). A SaltStack version will be published soon.</li>
</ul>
<h1>RESOURCES</h1>
<p>This section describes all the resources scanned by <strong>pysa</strong></p>
<p>By default, all item described are scanned. However, you can apply some filters to avoid or specify some. See the FILTERS_ section.</p>
<p>At the current state, the resources objects and keys are similar to Puppet types. Jump to <em>pysa/scanner/object/</em> for a compelte object description. These objects will be documented soon.</p>
<p>Please see AUTOCONF TOOLS MODULES_ section to be sure to be able to handle all scanned resources.</p>
<p>Pleese note that in main cases, the scan must be done by an admin user (mostly root).</p>
<h2>configuration files - file</h2>
<p><strong>pysa</strong> scans (and stores in output module) all files located in a specific location. Default <strong>/etc</strong> and <strong>/root/.ssh</strong></p>
<p>Primary key: <em>path</em></p>
<h2>packages - package</h2>
<p><strong>pysa</strong> is able to scan all packages provided by <em>yum</em>, <em>apt-get</em>, python pypi (<em>pip</em>), ruby <em>gems</em>, nodejs packaged modules (<em>npm</em>) and php packages managers (<em>pear</em> and <em>pecl</em>).</p>
<p>Furthermore, <strong>pysa</strong> is able to detect repositories <em>rpm</em> packages if <em>yum</em> is not present.</p>
<p>Primary key: <em>name</em></p>
<h2>services - service</h2>
<p><strong>pysa</strong> detects all startup services managed by <em>upstart</em> and <em>SysV init</em> scripts.</p>
<p>Please see NOTES_ section.</p>
<p>Primary key: <em>name</em></p>
<h2>hosts - host</h2>
<p><strong>pysa</strong> scans and reproduces existing hostname associations (default <em>/etc/hosts</em>).</p>
<p>Primary key: <em>name</em></p>
<h2>users - user</h2>
<p><strong>pysa</strong> scans and reproduces existing users (<em>/etc/passwd</em>).</p>
<p>Primary key: <em>name</em></p>
<h2>groups - group</h2>
<p><strong>pysa</strong> scans and reproduces existing groups (<em>/etc/groups</em>).</p>
<p>Primary key: <em>name</em></p>
<h2>mounts - mount</h2>
<p><strong>pysa</strong> scans and reproduces existing mount points (<em>/etc/fstab</em>).</p>
<p>Primary key: <em>device</em></p>
<h2>crons - cron</h2>
<p><strong>pysa</strong> scans and reproduces user’s crons.</p>
<p>Primary key: <em>name</em></p>
<h2>ssh keys - key</h2>
<p><strong>pysa</strong> scans and reproduces root SSH keys (default <em>/root/.ssh</em>).</p>
<p>SSH keys are manages as files.</p>
<p>Primary key: <em>name</em></p>
<h2>sources repositories - source</h2>
<p><strong>pysa</strong> is able to recognize all source repositories managed by the most common SCM (<em>subversion</em>, <em>git</em> and <em>mercurial</em>) present in the system.</p>
<p>Primary key: <em>path</em></p>
<p><strong>Puppet only</strong> The sources scanner is not able to scan sources repositories for SaltStack yet.</p>
<h2>package managers repositories - repository</h2>
<p><strong>pysa</strong> scans and reproduces <em>yum</em> and <em>apt-get</em> repositories.</p>
<p>Primary key: <em>name</em></p>
<h1>AUTOCONF TOOLS MODULES</h1>
<p>This section lists the autoconf tools’ modules which may be used.</p>
<p>Modules are used for particular features and are only needed in some particular cases. Of course, modules (as with the autoconf tools) have to be installed on the new machine, not the original one.</p>
<h2>Puppet modules</h2>
<p>willdurand/nodejs: add <em>npm</em> package manager support nodes/php: add <em>php</em> package manager support puppetlabs/vcsrepo: add <em>scm</em> (sources) support</p>
<p>to install a Puppet module: puppet module install <em>module-name</em></p>
<h1>FILTERS</h1>
<p><strong>pysa</strong> integrates a powerful filters engine, which allows you to adapt its behavior to your needs.</p>
<p>A filter file is composed of sections, keys and values. In some specific cases sections and/or keys can be split using a ‘.’ (see below for more details).</p>
<p>A key can be tagged with ‘_’ at the front to be considered as “action” key. An action key is a key representing a specific action in the section (see below).</p>
<p>If some parameters conflict then the result may be harmful, please use it carefully. Don’t hesitate to report any abnormal output to us.</p>
<p>Some improvements are planned in this section.</p>
<h2>common action keys</h2>
<h3>_contentrefer</h3>
<p>This key acts as a pointer. All the content of the referred section will be interpreted in the section.</p>
<p>This key should be set alone, as all keys will be replaced.</p>
<h2>addition section</h2>
<h3>addition section description</h3>
<p>This section is used to add or modify some values.</p>
<p>It can sounds similar to the replace section, but works in a completely different way:</p>
<ul>
<li>The key is based on section key instead of content to replace</li>
<li>It is replaced at the scanning step, while the <em>replacement</em> section is done at the output generation step</li>
</ul>
<p>Remember that <em>addition</em> is used to add/set a concrete parameter, while <em>replace</em> is used to replace some content.</p>
<p>The section name can be separate in multiple subsections using a dot ‘.’, always starting by <em>addition</em> keyword:</p>
<ul>
<li>addition.resource_type will replace values for all objects of resource_type</li>
<li>addition.resource_type.key.value will replace only the values for the objects where the key/value match the requirement</li>
</ul>
<p>The key represents the resource key. The value represents the resource value.</p>
<h3>addition section format</h3>
<p>section_key = section_value</p>
<h3>addition section action keys</h3>
<p>No action key for this section.</p>
<h2>discard section</h2>
<h3>discard section description</h3>
<p>This section is used to specify which object should or shouldn’t be discard.</p>
<p>The key is separated in to two sub-keys by a dot ‘.’, which represents the object type for the first one and the attribute name for the second one.</p>
<p>The values can be seen as a list of attributes separated by a coma ‘,’.</p>
<p>The joker ‘*’ can be used to specify to match all characters.</p>
<h3>discard section format</h3>
<p>object.attribute_name = attribute1, attribute2*, …</p>
<h3>discard section action keys</h3>
<dl>
<dt>_resources:</dt>
<dd><p>resource names Select which resources to be scanned, use it carefully, some resources might depend on others.</p>
</dd>
</dl>
<h2>replace section</h2>
<h3>replace section description</h3>
<p>This section is used to replace any kind of content.</p>
<p>The section name can be separated into multiple subsections using a dot ‘.’, always starting by <em>replace</em> keyword:</p>
<ul>
<li>replace will replace all values for all objects.</li>
<li>replace.object will replace all values for the selected object.</li>
<li>replace.object.field will replace only the values associated with the field in the selected object.</li>
</ul>
<p>The key represents the new value. The value(s) represents the target to replace.</p>
<h3>replace section format</h3>
<p>new_value = old_value1, old_value2, …</p>
<h3>replace section action keys</h3>
<p>_replaceall:</p>
<ul>
<li>true/false</li>
<li>REQUIRED</li>
<li>Select the filtering mode (replace all except -true- or replace none except -false-)</li>
<li>default: true _except: primary_keys_values</li>
</ul>
<h2>update section</h2>
<h3>update section description</h3>
<p>This section is used to specify which <em>package</em> should be updated. This section has been created due to the lack of old packages in many repositories.</p>
<p>A list of package names is specified as values of the <em>except</em> key, separated by a coma ‘,’.</p>
<p>The joker ‘*’ can be used to specify to match all characters.</p>
<h3>update section format</h3>
<p>except = package1, package2*, *package3, *package4*, …</p>
<h3>update section action keys</h3>
<p>_update:</p>
<ul>
<li>true/false</li>
<li>REQUIRED</li>
<li>Select the filtering mode (update all except -true- or update none except -false-)</li>
<li>default: false</li>
</ul>
<h1>USAGE EXAMPLES</h1>
<p>See <em>docs/examples</em> for configuration file examples.</p>
<h1>NOTES</h1>
<p><strong>pysa</strong> has been inspired by a software called <em>Blueprint</em> (more information at <a href="http://devstructure.com/blueprint/"><a href="http://devstructure.com/blueprint/">http://devstructure.com/blueprint/</a></a>).</p>
<p>The force of <strong>pysa</strong> lies on the following points:</p>
<ul>
<li><strong>pysa</strong>’s “filters” and <em>Blueprint</em>’s “rules” are totally different. Please refer to the documentations for more details.</li>
<li><strong>pysa</strong>’s <em>Puppet</em> output is cleaner (the files are separated, the module is automatically created…).</li>
<li>The dependency cycle is more resilient. <strong>pysa</strong> generates an attribute-based dependency cycle (each object relies and depends on its own dependencies) so if something fails the whole process isn’t stopped.</li>
<li><strong>pysa</strong> is under active development and there is additional functionality under development (e.g., integration to <em>Madeira</em>’s services, <em>Salt</em>/<em>Chef</em> modules).</li>
</ul>
<p>As an early-release, <strong>pysa</strong> does not (always) provide 100% functional results. This comes, in some cases, from the architectural choices that we’ve made. For example, <strong>pysa</strong> does not (yet) support the addition of user’s packages, simply because we can’t ensure the availability of these packages on the new system. It would lead to the generation of wrong output files.</p>
<p>Furthermore, <strong>pysa</strong> depends on “autoconf” tools. This means that if a feature is not supported by one of these tools, <strong>pysa</strong> can’t provide it. For example, it is currently impossible to use upstart services on a <em>Redhat</em> based platform, as it is impossible to use npm package manager on <em>Ubuntu</em>.</p>
<p>Please don’t hesitate to contact us for any kind of feedback, advice or requirement: <script type="text/javascript">
<!--
h='&#x67;&#x6f;&#x6f;&#x67;&#108;&#x65;&#x67;&#114;&#x6f;&#x75;&#112;&#x73;&#46;&#x63;&#x6f;&#x6d;';a='&#64;';n='&#112;&#x79;&#x73;&#x61;&#x2d;&#x75;&#x73;&#x65;&#114;';e=n+a+h;
document.write('<a h'+'ref'+'="ma'+'ilto'+':'+e+'">'+e+'<\/'+'a'+'>');
// -->
</script><noscript>&#112;&#x79;&#x73;&#x61;&#x2d;&#x75;&#x73;&#x65;&#114;&#32;&#x61;&#116;&#32;&#x67;&#x6f;&#x6f;&#x67;&#108;&#x65;&#x67;&#114;&#x6f;&#x75;&#112;&#x73;&#32;&#100;&#x6f;&#116;&#32;&#x63;&#x6f;&#x6d;</noscript> for public discussions and <script type="text/javascript">
<!--
h='&#x6d;&#x63;&#50;&#46;&#x69;&#x6f;';a='&#64;';n='&#112;&#x79;&#x73;&#x61;';e=n+a+h;
document.write('<a h'+'ref'+'="ma'+'ilto'+':'+e+'">'+e+'<\/'+'a'+'>');
// -->
</script><noscript>&#112;&#x79;&#x73;&#x61;&#32;&#x61;&#116;&#32;&#x6d;&#x63;&#50;&#32;&#100;&#x6f;&#116;&#32;&#x69;&#x6f;</noscript> for private messages.</p>
<p>If you have a question about a specific source file, you can also contact the author directly (<script type="text/javascript">
<!--
h='&#x6d;&#x63;&#50;&#46;&#x69;&#x6f;';a='&#64;';n='&#102;&#x69;&#114;&#x73;&#116;&#x2d;&#110;&#x61;&#x6d;&#x65;';e=n+a+h;
document.write('<a h'+'ref'+'="ma'+'ilto'+':'+e+'">'+e+'<\/'+'a'+'>');
// -->
</script><noscript>&#102;&#x69;&#114;&#x73;&#116;&#x2d;&#110;&#x61;&#x6d;&#x65;&#32;&#x61;&#116;&#32;&#x6d;&#x63;&#50;&#32;&#100;&#x6f;&#116;&#32;&#x69;&#x6f;</noscript>)</p>
<h1>BUGS</h1>
<p>No known bugs.</p>
</body>
</html>
