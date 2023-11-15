// 将JS源码转换成语法树
const parser = require("@babel/parser");
// 遍历并处理AST
const traverse = require("@babel/traverse").default;
// 操作节点，比如判断节点类型，生成新的节点等
const t = require("@babel/types");
// 将语法树转换为源代码
const generator = require("@babel/generator").default;
// 操作文件
const fs = require("fs");

// 读取混淆代码
var jscode = fs.readFileSync("ac.js", {
    encoding: "utf-8"
});
// 将代码转换为AST语法树
let ast = parser.parse(jscode);
console.log(ast)


function ergodic(ast) {
    for (let i in ast) {
        if (ast.type == "StringLiteral") {
            console.log(ast.value)
            ast.extra.raw = ast.value
            return void 0
        }

        if (typeof ast[i] == "object") {
            ergodic(ast[i])
        }
    }
}
// ergodic(ast)

traverse(
    ast, {
        StringLiteral: function (path) {
            // console.log(path)
        }
})

const { code: output } = generator(ast);
console.log(output);
