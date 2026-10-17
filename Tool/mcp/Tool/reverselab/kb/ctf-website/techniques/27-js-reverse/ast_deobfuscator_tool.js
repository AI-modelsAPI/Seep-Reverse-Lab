#!/usr/bin/env node
/**
 * ast_deobfuscator_tool.js — 现代 JavaScript AST 自动化工业级解混淆引擎
 * 
 * 核心增强能力：
 * 1. 字符与字面量还原（十六进制/Unicode 格式擦除）
 * 2. 成员访问计算属性规范化 (obj['foo'] -> obj.foo)
 * 3. 表达式常量折叠与求值计算 (1 + 2 -> 3, ![] -> false)
 * 4. 消除对象花指令代理函数（如 _0x12['add'] = function(a, b) { return a + b } 自动内联还原）
 * 5. 控制流平坦化消除（While-Switch 状态机调度重构为原生顺序执行流）
 * 6. 逗号表达式（SequenceExpression）打平展开为独立语句
 * 7. 死代码与无用分支剔除 (if (false) { ... })
 */

const fs = require('fs');
const path = require('path');

// 兼容全局与本地 NODE_PATH 寻址
try {
    require('@babel/parser');
} catch (e) {
    const globalNodeModules = require('child_process')
        .execSync('npm root -g', { encoding: 'utf-8' }).trim();
    module.paths.push(globalNodeModules);
}

const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const generator = require('@babel/generator').default;
const t = require('@babel/types');

function deobfuscate(sourceCode) {
    console.log("[*] 解析抽象语法树 (AST)...");
    const ast = parser.parse(sourceCode, {
        sourceType: "unambiguous",
        plugins: ["jsx", "typescript"]
    });

    // ── 规则 1: 规范化十六进制与 Unicode 字符字面量 ──
    console.log("[1/7] 规范化字符编码与数值字面量...");
    traverse(ast, {
        StringLiteral(path) {
            if (path.node.extra && path.node.extra.raw) {
                delete path.node.extra.raw;
            }
        },
        NumericLiteral(path) {
            if (path.node.extra && path.node.extra.raw) {
                delete path.node.extra.raw;
            }
        }
    });

    // ── 规则 2: 计算属性转直接点号成员访问 (obj['foo'] -> obj.foo) ──
    console.log("[2/7] 计算属性成员访问规范化...");
    traverse(ast, {
        MemberExpression(path) {
            const prop = path.node.property;
            if (path.node.computed && t.isStringLiteral(prop)) {
                if (/^[a-zA-Z_$][a-zA-Z0-9_$]*$/.test(prop.value)) {
                    path.node.computed = false;
                    path.node.property = t.identifier(prop.value);
                }
            }
        }
    });

    // ── 规则 3: 表达式常量折叠与求值计算 (1 + 2 -> 3, ![] -> false) ──
    console.log("[3/7] 表达式常量折叠与布尔运算求值...");
    traverse(ast, {
        "BinaryExpression|UnaryExpression"(path) {
            const res = path.evaluate();
            if (res.confident) {
                if (typeof res.value === 'string') {
                    path.replaceWith(t.stringLiteral(res.value));
                } else if (typeof res.value === 'number') {
                    path.replaceWith(t.numericLiteral(res.value));
                } else if (typeof res.value === 'boolean') {
                    path.replaceWith(t.booleanLiteral(res.value));
                }
            }
        }
    });

    // ── 规则 4: 消除对象别名花指令与代理调用 (Object Proxy Functions) ──
    console.log("[4/7] 提取并消除对象别名代理函数 (花指令内联还原)...");
    let proxyInlineCount = 0;
    traverse(ast, {
        VariableDeclarator(path) {
            const { id, init } = path.node;
            if (!t.isIdentifier(id) || !t.isObjectExpression(init)) return;

            const objName = id.name;
            const scope = path.scope;
            const binding = scope.getBinding(objName);
            if (!binding || !binding.constant) return;

            const fnMap = new Map();
            for (const prop of init.properties) {
                if (!t.isObjectProperty(prop)) continue;
                const key = t.isIdentifier(prop.key) ? prop.key.name : (t.isStringLiteral(prop.key) ? prop.key.value : null);
                if (!key) continue;

                // Case A: 代理普通字符串/常量
                if (t.isStringLiteral(prop.value)) {
                    fnMap.set(key, { type: 'literal', value: prop.value });
                }
                // Case B: 代理简单二元运算函数: function(a, b) { return a + b; }
                else if (t.isFunctionExpression(prop.value) || t.isArrowFunctionExpression(prop.value)) {
                    const fn = prop.value;
                    if (t.isBlockStatement(fn.body) && fn.body.body.length === 1) {
                        const retStmt = fn.body.body[0];
                        if (t.isReturnStatement(retStmt)) {
                            fnMap.set(key, { type: 'fn', params: fn.params, returnVal: retStmt.argument });
                        }
                    }
                }
            }

            if (fnMap.size === 0) return;

            // 替换该对象在当前作用域内的所有调用点
            for (const refPath of binding.referencePaths) {
                const parent = refPath.parentPath;
                if (!parent || !parent.isMemberExpression()) continue;

                const propNode = parent.node.property;
                const propKey = t.isIdentifier(propNode) ? propNode.name : (t.isStringLiteral(propNode) ? propNode.value : null);
                const info = fnMap.get(propKey);
                if (!info) continue;

                // 替换调用: obj.add(a, b) -> a + b
                if (info.type === 'fn') {
                    const callPath = parent.parentPath;
                    if (callPath && callPath.isCallExpression() && callPath.node.callee === parent.node) {
                        const callArgs = callPath.node.arguments;
                        // 克隆返回表达式并替换形参
                        const clonedExpr = t.cloneNode(info.returnVal);
                        const paramNames = info.params.map(p => p.name);
                        
                        // 简单二元/二元逻辑替换
                        if (t.isBinaryExpression(clonedExpr) || t.isLogicalExpression(clonedExpr)) {
                            const leftIdx = paramNames.indexOf(clonedExpr.left.name);
                            const rightIdx = paramNames.indexOf(clonedExpr.right.name);
                            if (leftIdx !== -1 && rightIdx !== -1) {
                                callPath.replaceWith(t.binaryExpression(clonedExpr.operator, callArgs[leftIdx], callArgs[rightIdx]));
                                proxyInlineCount++;
                            }
                        } else if (t.isCallExpression(clonedExpr) && t.isIdentifier(clonedExpr.callee)) {
                            // 调用代理: obj.call(fn, arg1) -> fn(arg1)
                            const fnIdx = paramNames.indexOf(clonedExpr.callee.name);
                            if (fnIdx !== -1) {
                                const realFn = callArgs[fnIdx];
                                const restArgs = callArgs.slice(1);
                                callPath.replaceWith(t.callExpression(realFn, restArgs));
                                proxyInlineCount++;
                            }
                        }
                    }
                } else if (info.type === 'literal') {
                    parent.replaceWith(t.cloneNode(info.value));
                    proxyInlineCount++;
                }
            }
        }
    });
    console.log(`    -> 成功内联消除了 ${proxyInlineCount} 处花指令对象代理调用`);

    // ── 规则 5: 控制流平坦化消除 (While-Switch 调度消除) ──
    console.log("[5/7] 检测并消除控制流平坦化 (While-Switch 调度展开)...");
    let unflattenCount = 0;
    traverse(ast, {
        WhileStatement(path) {
            const test = path.node.test;
            if (!(t.isBooleanLiteral(test, { value: true }) || t.isNumericLiteral(test, { value: 1 }))) {
                return;
            }

            const body = path.node.body;
            if (!t.isBlockStatement(body) || body.body.length === 0) return;

            const switchNode = body.body[0];
            if (!t.isSwitchStatement(switchNode)) return;

            const prevSibling = path.getPrevSibling();
            if (!prevSibling || !prevSibling.isVariableDeclaration()) return;

            let orderString = null;
            prevSibling.traverse({
                StringLiteral(subPath) {
                    const val = subPath.node.value;
                    if (val.includes("|") && val.length > 1) {
                        orderString = val;
                    }
                }
            });

            if (!orderString) return;

            const orders = orderString.split("|");
            const cases = switchNode.cases;
            const caseMap = new Map();

            for (const c of cases) {
                const key = c.test ? (t.isStringLiteral(c.test) ? c.test.value : (t.isNumericLiteral(c.test) ? String(c.test.value) : null)) : null;
                const statements = c.consequent.filter(stmt => {
                    return !t.isContinueStatement(stmt) && !t.isBreakStatement(stmt);
                });
                caseMap.set(String(key), statements);
            }

            const unflattenedBody = [];
            for (const step of orders) {
                const stmts = caseMap.get(step);
                if (stmts) {
                    unflattenedBody.push(...stmts);
                }
            }

            if (unflattenedBody.length > 0) {
                path.replaceWithMultiple(unflattenedBody);
                if (prevSibling && prevSibling.isVariableDeclaration()) {
                    prevSibling.remove();
                }
                unflattenCount++;
            }
        }
    });
    console.log(`    -> 成功还原了 ${unflattenCount} 处控制流平坦化结构`);

    // ── 规则 6: 展开独立逗号表达式为顺序语句 (SequenceExpression to Statements) ──
    console.log("[6/7] 展开语句级逗号表达式 (SequenceExpression Flattener)...");
    let seqCount = 0;
    traverse(ast, {
        ExpressionStatement(path) {
            const expr = path.node.expression;
            if (t.isSequenceExpression(expr)) {
                const statements = expr.expressions.map(subExpr => t.expressionStatement(subExpr));
                path.replaceWithMultiple(statements);
                seqCount++;
            }
        }
    });
    console.log(`    -> 成功将 ${seqCount} 处逗号表达式规整为独立顺序语句`);

    // ── 规则 7: 死代码与无用分支剔除 (if (false) { ... }) ──
    console.log("[7/7] 剔除无用死代码分支...");
    traverse(ast, {
        IfStatement(path) {
            const test = path.node.test;
            if (t.isBooleanLiteral(test)) {
                if (test.value === true) {
                    path.replaceWith(path.node.consequent);
                } else if (test.value === false) {
                    if (path.node.alternate) {
                        path.replaceWith(path.node.alternate);
                    } else {
                        path.remove();
                    }
                }
            }
        }
    });

    console.log("[*] 重建格式化纯净代码...");
    const output = generator(ast, {
        comments: true,
        retainLines: false,
        compact: false
    });

    return output.code;
}

// ── 命令行入口 ──
const args = process.argv.slice(2);
if (args.length === 0 || args.includes('-h') || args.includes('--help')) {
    console.log("用法: node ast_deobfuscator_tool.js <input.js> [-o output.js]");
    process.exit(0);
}

const inputFile = args[0];
let outputFile = null;
const outIdx = args.indexOf('-o');
if (outIdx !== -1 && args[outIdx + 1]) {
    outputFile = args[outIdx + 1];
}

if (!fs.existsSync(inputFile)) {
    console.error(`[-] 目标文件不存在: ${inputFile}`);
    process.exit(1);
}

const src = fs.readFileSync(inputFile, 'utf-8');
const result = deobfuscate(src);

if (outputFile) {
    fs.writeFileSync(outputFile, result, 'utf-8');
    console.log(`[+] 已成功写入解混淆成果至: ${outputFile}`);
} else {
    console.log("\n" + "=".repeat(60) + "\n");
    console.log(result.slice(0, 3000));
}
