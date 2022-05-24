<p>
    Dear All : &nbsp; &nbsp;&nbsp;
</p>
<p>
    &nbsp; &nbsp; &nbsp; &nbsp;为提升Gerrit服务器稳定性以及满足空间的需求，我们将从<span style="color: rgb(255, 0, 0);">11月16日（下周一）</span>开始统一切换到新服务器。新服务器的代码为旧服务器11/14日最新的版本。为保证代码统一，原服务器将同时停用。届时请大家花几分钟时间重新配置自已的Gerrit环境。
</p>
<p>
    &nbsp; &nbsp; &nbsp;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp;1. 使用以下用户名和密码登录新的Gerrit服务器: <a moz-do-not-send="true" href="http://gerrit.in.infotm.com/">http://gerrit.in.infotm.com</a>&nbsp;.
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;新的用户名密码为：<strong><em><span style="color:#E53333">&nbsp; </span></em><span style="color:#E53333">##USER_NAME</span></strong> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp; <span style="color: rgb(229, 51, 51);">##USER_PASS</span>&nbsp; &nbsp; &nbsp;&nbsp;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp;2. 点击右上角<strong>Anonymous Coward</strong> -&gt; <strong>Settings</strong> -&gt; <strong>Contact &nbsp;Information</strong>，添写自己的个人信息，如<span style="color: rgb(255, 0, 0);"><strong>##USER_FULL</strong></span>，(统一格式：英文名空格姓，首字母大写)。点击<strong>Register New Email</strong>，添写自己的邮箱：<strong><span style="color: rgb(255, 0, 0);">##USER_NAME</span></strong><span style="color: rgb(255, 0, 0);">@</span><strong><span style="color: rgb(255, 0, 0);">infotm.com</span></strong><strong style="white-space: normal;"><span style="color: rgb(255, 0, 0);"> &nbsp;</span></strong>(注意，请使用公司新邮箱)，最后点击<strong>Save Changes</strong>
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp;3. &nbsp;添加SSH Public Key，左边选则<strong>SSH Public Keys</strong>，执行命令&nbsp;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; $cat ~/.ssh/id_rsa.pub&nbsp;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 复制全部内容到gerrit ssh key文本框中，点击<strong>Add</strong>。 如果没有id_rsa.pub，使用以下命令生成：<em>&nbsp;</em>
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; $ ssh-keygen -t rsa &nbsp;-C &quot;<strong><span style="color:#E53333">##USER_NAME</span></strong><span style="color: rgb(255, 0, 0);">@</span><strong><span style="color:#ff0000">infotm.com</span></strong>&quot;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp;4. &nbsp;修改本地git配置：
</p>
<p class="MsoListParagraph">
    <em>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</em>$ git config --global user.name &nbsp; &quot;<strong><span style="color: rgb(255, 0, 0);">##USER_NAME</span></strong>&quot;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;$ git config --global user.email &nbsp;&quot;<strong><span style="color: rgb(255, 0, 0);">##USER_NAME</span></strong><span style="color: rgb(255, 0, 0);">@</span><strong><span style="color: rgb(255, 0, 0);">infotm.com</span></strong>&quot;&nbsp; &nbsp;&nbsp;<span style="background-color: rgb(248, 248, 248);">&nbsp;&nbsp;</span>
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp;5. &nbsp;更新本地repo，需要使用新的repo地址重新repo init ， 常用的repo地址可以从Wiki上检索：<a href="http://wiki.in.infotm.com/doku.php?id=internal_document:department:scheme:%E5%B8%B8%E7%94%A8%E4%BB%A3%E7%A0%81%E8%8E%B7%E5%8F%96" target="_blank" title="常用Repo地址">常用Repo地址</a>
</p>
<p class="MsoListParagraph">
    &nbsp;
</p>
<p class="MsoListParagraph">
    &nbsp; &nbsp; &nbsp; &nbsp;6. &nbsp;常见的repo使用的错误，也会在wiki上不定期更新，欢迎各位参阅和修订，也欢迎 大家把工作中的经验总结更新到<a href="http://wiki.in.infotm.com" target="_blank" title="Wiki">Wiki页面</a>。
</p>
<p class="MsoListParagraph">
    <br/>
</p>
<p class="MsoListParagraph">
    Enjoy It!
</p>
<p class="MsoListParagraph">
    Gerrit Admin
</p>
