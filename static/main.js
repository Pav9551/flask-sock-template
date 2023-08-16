var socket = io();

class Table{
  constructor(data){
    this.header = Object.keys(data)[0];
    this.status = data[this.header]["status"];
    this.body = (({ status, ...o }) => o)(data[this.header]);
    this.footer = data[this.header]["Счетчик"];
  }
  generate(){
    const header = `<tr><th>${this.header}</tr></th>`;
    const body = Object.keys(this.body).reduce((tr, td) => {
      tr += `<tr><td class='${this.body[td]}'>${td}</tr></td>`;
      return tr;
    }, "");
    const footer = `<tr><th>${this.footer}</tr></th>`;
    return header + body + footer;
  }
  create(table){
    table.className = this.status;
    table.innerHTML = this.generate();
    document.body.append(table);
  }
  update(table){
    table.className = this.status;
    table.innerHTML = this.generate();
  }
}

socket.on('sensors', function(msg) {
  const table = new Table(msg);
  const table_id = `room-${Object.keys(msg)[0]}`;
  const table_req = document.querySelector(`#${table_id}`);
  if(table_req){
    table.update(table_req);
  }else{
    const table_create = document.createElement("table");
    table_create.id = table_id;
    table.create(table_create);
  }
})
