/* tree.js  (no “export”) */

/* 1. parse flat TXT into event objects */
function parseModel1(raw) {
  const lines  = raw.trim().split(/\r?\n/);
  const events = [];
  for (let i = 0; i < lines.length; i += 2) {
    const depth   = Number(lines[i].trim());
    const summary = (lines[i+1]||'').trim();
    events.push({ id: i/2, depth, summary, children: [] });
  }
  return events;
}

/* 2. build hierarchical tree */
function buildTree(events) {
  const root  = { children: [] };
  const stack = [{ node: root, depth: -Infinity }];
  for (const ev of events) {
    while (ev.depth <= stack.at(-1).depth) stack.pop();
    const parent = stack.at(-1).node;
    ev.__parent = parent===root ? null : parent;
    parent.children.push(ev);
    stack.push({ node: ev, depth: ev.depth });
  }
  return root.children;
}

/* 3. render it into the UL#eventTree */
function labelFor(n) {
  const m = n.summary.match(/'([^']+)'/);
  const raw = m ? m[1] : n.summary;
  return raw.length>25 ? raw.slice(0,22)+'…' : raw;
}
function renderTree(tree, mountEl) {
  mountEl.innerHTML = '';
  (function walk(nodes, d){
    for(const n of nodes){
      const li = document.createElement('li');
      li.className = `depth-${d}`;
      li.textContent = labelFor(n);
      li.dataset.id = n.id;
      li.onclick = ()=> selectNode(n);
      mountEl.appendChild(li);
      walk(n.children, d+1);
    }
  })(tree,0);
}

/* 4. click behavior */
function selectNode(node) {
  document.querySelectorAll('#eventTree li')
    .forEach(li=>li.classList.toggle('current', li.dataset.id==node.id));
  document.getElementById('currentNote').textContent =
    node.summary;
  document.getElementById('currentDepthLabel').textContent =
    `Annotation (D:${node.depth})`;
  document.getElementById('parentAnnotation').value =
    node.__parent?.summary||'';
  const sib = node.__parent?.children?.find(c=>c!==node);
  document.getElementById('siblingAnnotation').value = sib?.summary||'';
}

/* 5. expose the loader as a global */
window.loadTxtAndBuildTree = function(rawTxt){
  const evs  = parseModel1(rawTxt);
  const tree = buildTree(evs);
  renderTree(tree, document.getElementById('eventTree'));
  if(evs.length) selectNode(evs[0]);
};