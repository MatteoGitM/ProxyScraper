class CountryCellRenderer {
  init(params) {
    const flag = `<img style="margin-right: 0.5rem" width="15" height="10" src="flags/${params.data.Country}.svg">`;
    const eTemp = document.createElement('div');
    eTemp.innerHTML = `<span>${flag}${params.value}</span>`;
    this.eGui = eTemp.firstElementChild;
  }

  getGui() {
    return this.eGui;
  }

  refresh(params) {
    return false;
  }
}
class SpeedCellRenderer {
  init(params) {
    const eTemp = document.createElement('div');
    eTemp.innerHTML = `<span>${params.value}s</span>`;
    this.eGui = eTemp.firstElementChild;
  }

  getGui() {
    return this.eGui;
  }

  refresh(params) {
    return false;
  }
}
class UptimeCellRenderer {
  init(params) {
    const eTemp = document.createElement('div');
    if (params.value <= 0) {
      eTemp.innerHTML = `<span>Connection lost ${params.value}</span>`;
    } else {
      eTemp.innerHTML = (params.value > 60) ? `<span>${Math.round(params.value / 60)}m</span>` : `<span>${params.value}s</span>`;
    }
    this.eGui = eTemp.firstElementChild;
  }

  getGui() {
    return this.eGui;
  }

  refresh(params) {
    return false;
  }
}

const gridOptions = {
  columnDefs: [
    { field: 'Country' , cellRenderer: CountryCellRenderer, maxWidth: 170, headerCheckboxSelection: true, checkboxSelection: true},
    { field: 'Proxy' , minWidth: 185},
    { field: 'Type' },
    { field: 'Tests' },
    { field: 'Anonymity' },
    { field: 'Speed', comparator: (A, B, X, Y, isDescending) => A - B, filter: 'agNumberColumnFilter', cellRenderer: SpeedCellRenderer },
    { field: 'Uptime', comparator: (A, B) => A - B, filter: 'agNumberColumnFilter', cellRenderer: UptimeCellRenderer, cellClass: params => {return params.value <= 0 ? 'row-fail' : '';}, },
    { field: 'HSTS' },
    { field: 'Spamhaus' },
  ],
  defaultColDef: {
    flex: 1,
    sortable: true,
    resizable: true,
    filter: true,
    menuTabs: ['filterMenuTab'],
  },
  rowSelection: 'multiple',
  enableRangeSelection: true,
  popupParent: document.querySelector('body'),
  getContextMenuItems: getContextMenuItems,
  getRowId: (params) => params.data.Proxy
};

function getContextMenuItems(params) {
  var result = [
    {
      name: 'Copy',
      action: function () {
        var checked_proxies = [];
        gridOptions.api.forEachNodeAfterFilter((rowNode, index) => {
          if (rowNode.selected) {  
            checked_proxies.push(rowNode.data.Proxy);
          }
        });
        navigator.clipboard.writeText(checked_proxies.join("\r\n"));
      }
    },
    {
      name: 'Export as .txt',
      action: function () {
        var checked_proxies = [];
        gridOptions.api.forEachNodeAfterFilter((rowNode, index) => {
          if (rowNode.selected) {        
            checked_proxies.push(rowNode.data.Proxy);
          }
        });
        var txt = checked_proxies.join('\r\n');
        var blob = new Blob([txt], { type: "text/plain;charset=utf-8" });
        saveAs(blob, "proxies.txt");
      }
    },
    'separator',
    {
      name: 'Delete',
      action: function () {
        gridOptions.api.forEachNodeAfterFilter((rowNode, index) => {
          if (rowNode.selected) {
            removeData(rowNode.data);
            eel.remove_proxy(rowNode.data.Proxy);
          }
        });
      }
    },
  ];

  return result;
}

function resultCallback() { console.log("updated"); }

eel.expose(updateData); 
function updateData(x) { gridOptions.api.applyTransaction({ update: [x] }, resultCallback); }

eel.expose(addData); 
function addData(x) { gridOptions.api.applyTransaction({ add: [x] }, resultCallback); }

eel.expose(removeData); 
function removeData(x) { gridOptions.api.applyTransaction({ remove: [x] }, resultCallback); }

eel.expose(updateLabel);
function updateLabel(x) {
    const lbl = document.querySelector('#status_bar');
    lbl.innerHTML = x;
}

eel.expose(updateRightLabel);
function updateRightLabel(x) {
    const lbl = document.querySelector('#status_right');
    lbl.innerHTML = x;
}

eel.expose(updateSettingsUI);
function updateSettingsUI(threads, timeouts, uptime, retries, socks5, socks4, http, a_remove, a_export, multi) {
  document.querySelector('#threads_select').value = threads;
  document.querySelector('#timeouts_select').value = timeouts;
  document.querySelector('#uptime_select').value = uptime;
  document.querySelector('#max_retries_select').value = retries;

  document.querySelector('#socks5_checkbox').checked = socks5;
  document.querySelector('#socks4_checkbox').checked = socks4;
  document.querySelector('#http_checkbox').checked = http;

  document.querySelector('#proxy_remove_toggle').checked = a_remove;
  document.querySelector('#auto_export_toggle').checked = a_export;
  document.querySelector('#multi_port_toggle').checked = multi;
}

eel.expose(updateVal);
function updateVal(x) {
    const json = JSON.parse(x);
    var id_list = [];

    for (const [key, value] of Object.entries(json)) {
      var id = Math.floor(Math.random() * 100).toString();
      var elem = document.querySelector('#badge-dismiss-dark');
      var clone = elem.cloneNode(true);
      clone.id = 'badge-dismiss-dark' + id;
      clone.innerHTML = clone.innerHTML.replace("Twitch.com", key);
      clone.innerHTML = clone.innerHTML.replaceAll('badge-dismiss-dark', 'badge-dismiss-dark' + id);
      clone.style.display = 'block';
      elem.after(clone);
      id_list.push(id);
    }

    id_list.forEach(function (item, index) {
      const btn_remove = document.querySelector('#button-badge-dismiss-dark' + item);
      btn_remove.addEventListener("click", () => {
        const span_val = document.querySelector('#badge-dismiss-dark' + item);
        span_val.style.display = 'none';
        eel.remove_validator_setting(span_val.innerText);
      });
    });
}

async function getData() { return []; }
// setup the grid after the page has finished loading
document.addEventListener('DOMContentLoaded', async function () {
  const gridDiv = document.querySelector('#myGrid');
  gridOptions.rowData = await getData();
  new agGrid.Grid(gridDiv, gridOptions);

  const navbar = document.querySelector('#navbar');
  const nav_button = document.querySelector('#nav_button');
  nav_button.addEventListener("click", () => {
    navbar.classList.toggle("translate-x-full");
  });

  const grid_click = document.querySelector('#myGrid');
  grid_click.addEventListener("click", () => {
    if (!navbar.classList.contains("translate-x-full")) {
      navbar.classList.toggle("translate-x-full");
    }
  });

  const valUrl = document.querySelector('#valLink');
  const valStr = document.querySelector('#valString');
  const add_val = document.querySelector('#valAdd');
  add_val.addEventListener("click", () => {
    updateVal('{"' + valUrl.value + '": "' + valStr.value + '"}');
    eel.add_validator_setting(valUrl.value, valStr.value);
    valUrl.value = "";
    valStr.value = "";
  });

  const lbl = document.querySelector('#status_bar');
  const start = document.querySelector('#start');
  start.addEventListener("click", () => {
    start.disabled = true;
    stop.disabled = false;
    lbl.innerHTML = "Starting...";
    eel.start_bot();
  });

  const stop = document.querySelector('#stop');
  stop.addEventListener("click", () => {
    start.disabled = false;
    stop.disabled = true;
    eel.stop_bot();
  });

  const download_proxies = document.querySelector('#download_proxies');
  download_proxies.addEventListener("click", () => {
    var proxies = [];
    gridOptions.api.forEachNodeAfterFilter((rowNode, index) => {      
        proxies.push(rowNode.data.Proxy);
    });
    var txt = proxies.join('\r\n');
    var blob = new Blob([txt], { type: "text/plain;charset=utf-8" });
    saveAs(blob, "proxies.txt");
  });

  
  const threads_select = document.querySelector('#threads_select');
  threads_select.addEventListener("change", () => {
    console.log(threads_select.value);
    eel.change_threads_setting(threads_select.value);
  });

  const timeouts_select = document.querySelector('#timeouts_select');
  timeouts_select.addEventListener("change", () => {
    eel.change_timeouts_setting(timeouts_select.value);
  });

  const uptime_select = document.querySelector('#uptime_select');
  uptime_select.addEventListener("change", () => {
    eel.change_uptime_setting(uptime_select.value);
  });

  const max_retries_select = document.querySelector('#max_retries_select');
  max_retries_select.addEventListener("change", () => {
    eel.max_retries_setting(max_retries_select.value);
  });

  const socks5_check = document.querySelector('#socks5_checkbox');
  const socks4_check = document.querySelector('#socks4_checkbox');
  const http_check = document.querySelector('#http_checkbox');
  socks5_check.addEventListener("change", () => {
    eel.change_socks5_setting(socks5_check.checked);
  });
  socks4_check.addEventListener("change", () => {
    eel.change_socks4_setting(socks4_check.checked);
  });
  http_check.addEventListener("change", () => {
    eel.change_http_setting(http_check.checked);
  });

  const auto_remove = document.querySelector('#proxy_remove_toggle');
  auto_remove.addEventListener("change", () => {
    eel.change_remove_setting(auto_remove.checked);
  });

  const auto_export = document.querySelector('#auto_export_toggle');
  auto_export.addEventListener("change", () => {
    eel.change_export_setting(auto_export.checked);
  });

  const multi_port_toggle = document.querySelector('#multi_port_toggle');
  multi_port_toggle.addEventListener("change", () => {
    eel.multi_port_setting(multi_port_toggle.checked);
  });

  const remove_filters = document.querySelector('#remove_filters');
  remove_filters.addEventListener("click", () => {
    gridOptions.api.setFilterModel(null);
    gridOptions.api.onFilterChanged();
  });

  eel.get_settings();
});
