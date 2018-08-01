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
    "actualStart": "2018-01-01",
    "actualEnd": "2018-12-31",
    "description": "\n[2018-01-01] created:\n[2018-01-01] status changed to open",
    "status": "open"
 },
"children": [
{
"treeDataItemData": {
    "id":2,
    "name": "[2] subtask",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-01-01",
    "actualEnd": "2018-06-30",
    "description": "\n[2018-01-01] created:\n[2018-01-01] status changed to open",
    "status": "open"
 },
"children": [
{
"treeDataItemData": {
    "id":3,
    "name": "[3] subsubtask1",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-01-01",
    "actualEnd": "2018-03-31",
    "progressValue": "50%",
    "description": "\n[2018-01-01] created:\n[2018-01-01] status changed to open",
    "status": "open"
 },
},
{
"treeDataItemData": {
    "id":4,
    "name": "[4] subsubtask2",
    "type": "sample",
    "member": "foo",
    "actualStart": "2018-05-31",
    "actualEnd": "2018-05-31",
    "description": "\n[2018-01-01] created",
    "status": "todo"
 },
}
]
}
]
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
var fifthColumn = dataGrid.column(4);
fifthColumn.labels().hAlign("left");
fifthColumn.title("status");
var hoge = fifthColumn.labels().format("{%status}");
var tooltip = dataGrid.tooltip();
tooltip.format("{%description}");
chart.rowSelectedFill('#FFFFCC');
chart.getTimeline().elements().selected().fill('#CCFF99');
var t1 = chart.getTimeline().lineMarker(0).value("current");
chart.container('container');
chart.draw();
chart.fitAll();
});