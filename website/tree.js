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

/* 2. build hierarchical tree using 0/1/-1 markers */
function buildTree(events) {
  const root = { children: [] };
  const stack = [root];

  events.forEach(ev => {
    const top = stack[stack.length - 1];
    ev.__parent = top === root ? null : top;

    if (ev.depth === 1) {
      // start a new goal block
      top.children.push(ev);
      stack.push(ev);
    } else if (ev.depth === -1) {
      // end current goal block (final child)
      top.children.push(ev);
      stack.pop();
    } else {
      // regular event (0) goes under current parent
      top.children.push(ev);
    }
  });

  return root.children;
}

/* 3. render into UL#eventTree */
function labelFor(n) {
  const m   = n.summary.match(/'([^']+)'/);
  const raw = m ? m[1] : n.summary;
  return raw.length > 25 ? raw.slice(0,22) + '…' : raw;
}

function renderTree(tree, mountEl) {
  mountEl.innerHTML = '';

  function walk(nodes, depth) {
    const ul = document.createElement('ul');
    ul.className = `depth-group depth-${depth}`;

    nodes.forEach(n => {
      const li = document.createElement('li');
      li.className = `depth-${depth}`;
      li.dataset.id = n.id;

      // click to select only this node
      li.addEventListener('click', e => {
        e.stopPropagation();
        window.currentSelectedNode = n;
        selectNode(n);
      });

      // arrow or spacer
      if (n.children.length) {
        const arrow = document.createElement('span');
        arrow.className = 'arrow';
        arrow.textContent = '▼';
        arrow.addEventListener('click', e => {
          e.stopPropagation();
          const childUl = li.querySelector('ul');
          const visible = childUl.style.display !== 'none';
          childUl.style.display = visible ? 'none' : '';
          arrow.textContent       = visible ? '▶' : '▼';
        });
        li.appendChild(arrow);
      } else {
        const spacer = document.createElement('span');
        spacer.className = 'arrow-spacer';
        li.appendChild(spacer);
      }

      // label text
      const label = document.createElement('span');
      label.className = 'label';
      label.textContent = labelFor(n);
      li.appendChild(label);

      // recurse into children
      if (n.children.length) {
        const [childUl] = walk(n.children, depth + 1);
        li.appendChild(childUl);
      }

      ul.appendChild(li);
    });

    return [ul];
  }

  const [rootUl] = walk(tree, 0);
  mountEl.appendChild(rootUl);
}

/* 4. select and highlight */
function selectNode(node) {
  // highlight
  document.querySelectorAll('#eventTree li')
    .forEach(li => li.classList.toggle('current', li.dataset.id == node.id));

  // current annotation
  document.getElementById('currentNote').textContent =
    node.summary;
  document.getElementById('currentDepthLabel').textContent =
    `Annotation (D:${node.depth})`;

  // parent annotation
  document.getElementById('parentAnnotation').value =
    node.__parent?.summary || '';

  // instead of sibling, show the very last (most recent) event loaded:
  const all = window._treeEvents || [];
  const last = all[all.length - 1];
  document.getElementById('siblingAnnotation').value =
    last?.summary || '';
}

/* 5. expose loader */
window.loadTxtAndBuildTree = function(rawTxt) {
  const evs  = parseModel1(rawTxt);
  window._treeEvents = evs;                    // ← stash full list
  const tree = buildTree(evs);
  renderTree(tree, document.getElementById('eventTree'));
  if (evs.length) selectNode(evs[0]);
};