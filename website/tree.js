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

  function walk(nodes, depth) {
    const ul = document.createElement('ul');
    ul.className = `depth-group depth-${depth}`;
    for (const n of nodes) {
      const li = document.createElement('li');
      li.className = `depth-${depth}`;
      li.dataset.id   = n.id;                // ← give it an ID

      // 1) stop clicks from bubbling past *this* node
      li.addEventListener('click', e => {
        e.stopPropagation();
        selectNode(n);
      });

      // arrow / spacer logic stays the same
      if (n.children.length) {
        const arrow = document.createElement('span');
        arrow.className = 'arrow';
        arrow.textContent = '▼';
        arrow.addEventListener('click', e => {
          e.stopPropagation();
          const childUl = li.querySelector('ul');
          const isVisible = childUl.style.display !== 'none';
          childUl.style.display   = isVisible ? 'none' : '';
          arrow.textContent       = isVisible ? '▶' : '▼';
        });
        li.appendChild(arrow);
      } else {
        li.appendChild(document.createElement('span'))
          .className = 'arrow-spacer';
      }

      // label
      const label = document.createElement('span');
      label.className = 'label'; 
      label.textContent = labelFor(n);
      li.appendChild(label);

      // recurse
      if (n.children.length) {
        walk(n.children, depth + 1).forEach(childUl =>
          li.appendChild(childUl)
        );
      }

      ul.appendChild(li);
    }
    return [ul];
  }

  const [rootUl] = walk(tree, 0);
  mountEl.appendChild(rootUl);
}

/* 4. click behavior */
function selectNode(node) {
  document.querySelectorAll('#eventTree li')
    .forEach(li => li.classList.toggle('current', li.dataset.id == node.id));
  document.getElementById('currentNote').textContent = node.summary;
  document.getElementById('currentDepthLabel').textContent =
    `Annotation (D:${node.depth})`;
  document.getElementById('parentAnnotation').value =
    node.__parent?.summary||'';
  const sib = node.__parent?.children?.find(c=>c!==node);
  document.getElementById('siblingAnnotation').value = sib?.summary||'';
}

/* 5. expose the loader as a global */
window.loadTxtAndBuildTree = function(rawTxt) {
  const evs  = parseModel1(rawTxt);
  const tree = buildTree(evs);
  renderTree(tree, document.getElementById('eventTree'));
  if (evs.length) selectNode(evs[0]);
};