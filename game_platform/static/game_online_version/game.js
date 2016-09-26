var mark = new Array(9);
for (var i = 0; i < 9; i++) {
    mark[i] = new Array(9);
}
var x = new Array(9);
for (var i = 0; i < 9; i++) {
    x[i] = new Array(9);
}
var direction = [[-1, 0], [0, 1], [1, 0], [0, -1]];
var findThree = 1;
var highscore = 0;
var numberOfJewels = 4;

function dfs(row, column, jewelColor) {
    mark[row][column] = 1;
    for (var i = 0; i < 4; i++) {
        if (row + direction[i][0] >= 0 && row + direction[i][0] <= 8 && column + direction[i][1] >= 0 && column + direction[i][1] <= 8) {
            if (x[row + direction[i][0]][column + direction[i][1]] == jewelColor && mark[row + direction[i][0]][column + direction[i][1]] == 0) {
                findThree++;
                dfs(row + direction[i][0], column + direction[i][1], jewelColor);
            }
        }
    }
}

function checkAllThree() {
    for (var i = 0; i < 9; i++) {
        for (var j = 0; j < 9; j++) {
            if (mark[i][j] == 0) {
                findThree = 1;
                dfs(i, j, x[i][j]);
                if (findThree >= 3) {
                    return '' + i + j; //e.g. 47 is for row 5 and column 8, which is connected with more than 2 jewels
                }
            }
        }
    }
    return -1; //didnt find any three connected jewels
}


function getPic(i,j) {
    var picture;
    switch (x[i][j]) {
        case 1:
            picture = "https://googledrive.com/host/0B7nXLbUyLD5eX0taQmVpQi1SRHc";
            break;
        case 2:
            picture = "https://googledrive.com/host/0B7nXLbUyLD5eQm1LOGsxcTVhTzQ";
            break;
        case 3:
            picture = "https://googledrive.com/host/0B7nXLbUyLD5eaTdZU3Jlb1ZQNVU";
            break;
        case 4:
            picture = "https://googledrive.com/host/0B7nXLbUyLD5ea2MyZzJiU01YOFk";
            break;
        default:
            picture = "https://googledrive.com/host/0B7nXLbUyLD5ea2MyZzJiU01YOFk";
            break;
    }
    return picture;
}

function refreshBoard() {
    for (var i = 0; i < 9; i++) {
        for (var j = 0; j < 9; j++) {
            var pic = getPic(i, j);
            $('#' + i + j + ' img').attr("src", pic);
        }
    }
}

function refreshMark() {
    for (var i = 0; i < 9; i++) {
        for (var j = 0; j < 9; j++) {
            mark[i][j] = 0;
        }
    }
}

function changeMarkedJewels() {
    for (var i = 0; i < 9; i++) {
        for (var j = 0; j < 9; j++) {
            if (mark[i][j] == 1) {
                x[i][j] = Math.floor(Math.random() * numberOfJewels) + 1;
                mark[i][j] = 0;
                highscore += 1;
            }
        }
    }
    $('#score').val(highscore);
}

function exitDeadEnd() {
    while (checkAllThree() == -1) {//if there are no three or more adjacent left and the game got stuck
        x[Math.floor(Math.random() * 9)][Math.floor(Math.random() * 9)] = Math.floor(Math.random() * numberOfJewels) + 1;
        refreshMark();
    }
}

$(document).ready(function () {

    for (var i = 0; i < 9; i++) {
        $('#board table').append('\n\t <tr>');
        for (var j = 0; j < 9; j++) {
            mark[i][j] = 0;
            x[i][j] = Math.floor(Math.random() * numberOfJewels) + 1;
            var pic = getPic(i, j);
            $('#board table tr:last-child').append('\n\t <td id=\"' + i + j + '\"> <img src=\"' + pic + '\" alt=\"\" width=\"25\" height=\"25\"> </td>');
        }
    }

    $('#board table').on('click', 'td', function () {
        refreshMark();
        var row_column = $(this).attr('id');
        var r = Math.floor(parseInt(row_column) / 10);
        var c = Math.floor(parseInt(row_column) % 10);
        findThree = 1;
        dfs(r, c, x[r][c]);
        if (findThree >= 3) {
            //for (var i = 0; i < 9; i++) {
            //for (var j = 0; j < 9; j++) {
            //$('#score').value += mark[i][j];
            //} 
            //$('#score').value += '\n';
            //} 
            changeMarkedJewels();
            exitDeadEnd();
        }
        refreshBoard();
    });
});



