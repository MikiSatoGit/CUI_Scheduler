var chart;
anychart.onDocumentReady(function () {
var json = {
    "gantt": {
        "type": "project",
        "controller": {
            "treeData": {
                "children": [
                    {
"treeDataItemData": {
    "id":1,
    "name": "[1] maintask",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-12-31",
    "actualEnd": "2018-12-31"
},
"children": [{
"treeDataItemData": {
    "id":2,
    "name": "[2] subtask",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-12-31",
    "actualEnd": "2018-12-31"
},
"children": [{
"treeDataItemData": {
    "id":3,
    "name": "[3] subsubtask1",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-12-31",
    "actualEnd": "2018-12-31"
},
},{
"treeDataItemData": {
    "id":4,
    "name": "[4] subsubtask2",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-12-31",
    "actualEnd": "2018-12-31"
},
}]
}]
                    }
                ]
            }
        }
    }
};
chart = anychart.fromJson(json);
var dataGrid = chart.dataGrid();
var thirdColumn = dataGrid.column(2);
thirdColumn.labels().hAlign("left");
thirdColumn.title("Type");
thirdColumn.labels().format("{%type}");
var forthColumn = dataGrid.column(3);
forthColumn.labels().hAlign("left");
forthColumn.title("Member");
forthColumn.labels().format("{%member}");
chart.container('container');
chart.draw();
chart.fitAll();
});