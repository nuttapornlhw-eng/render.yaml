async function scan() {
  const payload = {
    keyword: document.getElementById('keyword').value.trim(),
    target_url: document.getElementById('target_url').value.trim(),
    min_dr: Number(document.getElementById('min_dr').value),
    min_ur: Number(document.getElementById('min_ur').value),
    min_da: Number(document.getElementById('min_da').value),
    min_pa: Number(document.getElementById('min_pa').value),
    max_spam: Number(document.getElementById('max_spam').value),
    top_n: Number(document.getElementById('top_n').value),
    use_serpapi: document.getElementById('use_serpapi').checked
  };
  const status = document.getElementById('status');
  status.textContent = 'กำลังประมวลผล...';
  const res = await fetch('/scan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  status.textContent = `พบ ${data.count} เว็บไซต์ที่ผ่านเกณฑ์`;
  const tbody = document.querySelector('#resultTable tbody');
  tbody.innerHTML = '';
  (data.items || []).forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="p-2">${row.domain}</td>
      <td class="p-2 text-right">${row.dr}</td>
      <td class="p-2 text-right">${row.ur}</td>
      <td class="p-2 text-right">${row.da}</td>
      <td class="p-2 text-right">${row.pa}</td>
      <td class="p-2 text-right">${row.spam_score}</td>
      <td class="p-2 text-right">${row.score ? row.score.toFixed(3) : ''}</td>
    `;
    tbody.appendChild(tr);
  });
  const exportWrap = document.getElementById('exportWrap');
  const exportLink = document.getElementById('exportLink');
  exportWrap.classList.remove('hidden');
  exportLink.href = data.download;
}

document.getElementById('scanBtn').addEventListener('click', scan);
