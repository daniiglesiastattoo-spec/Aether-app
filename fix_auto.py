c = open('aether_final.py').read()
old = '</style></head>'
new = '''</style>
<script>
function enviar(){
  var msg = document.getElementById("inp").value.trim();
  if(!msg) return;
  document.getElementById("frm").submit();
}
document.addEventListener("DOMContentLoaded", function(){
  var inp = document.getElementById("inp");
  if(inp) inp.focus();
});
</script></head>'''
c = c.replace(old, new)
old2 = '<input type="submit" value="ENVIAR"'
new2 = '<input type="submit" value="ENVIAR" onclick="this.value=\'Espera...\';this.style.opacity=\'0.5\'"'
c = c.replace(old2, new2)
open('aether_final.py','w').write(c)
print("OK")
