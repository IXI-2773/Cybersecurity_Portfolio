const assert = require('node:assert/strict');
const {evaluateCR, evaluateRAI} = require('../assets/js/portfolio-systems.js');
let checks = 0;
function check(name, fn) { fn(); checks++; }
check('original available', () => assert.equal(evaluateCR({asOf:'2026-03-10', revision:false}).eligible,true));
check('later revision held', () => assert.equal(evaluateCR({asOf:'2026-03-10', revision:true}).eligible,false));
check('exact release accepted', () => assert.equal(evaluateCR({asOf:'2026-03-20', revision:true}).eligible,true));
check('before original release held', () => assert.equal(evaluateCR({asOf:'2026-03-03', revision:false}).eligible,false));
check('original never overwritten', () => assert.equal(evaluateCR({asOf:'2026-03-25', revision:false}).value,'2.4'));
check('revision value distinct', () => assert.equal(evaluateCR({asOf:'2026-03-25', revision:true}).value,'2.7'));
for (const asOf of ['2026-02-30', '', 'wrong', '2026-3-20', null]) {
  check('invalid date held '+asOf, () => assert.equal(evaluateCR({asOf,revision:true}).eligible,false));
}
check('conflict preserved', () => assert.equal(evaluateRAI({includeB:true,attributionValid:true,agrees:false}).state,'conflict'));
check('missing coverage held', () => assert.equal(evaluateRAI({includeB:false,attributionValid:true,agrees:true}).state,'missing'));
check('bad attribution held', () => assert.equal(evaluateRAI({includeB:true,attributionValid:false,agrees:true}).state,'attribution'));
check('support only with both sources', () => assert.equal(evaluateRAI({includeB:true,attributionValid:true,agrees:true}).state,'supported'));
check('unknown input not supported', () => assert.notEqual(evaluateRAI({}).state,'supported'));
check('missing outranks apparent agreement', () => assert.equal(evaluateRAI({includeB:false,attributionValid:false,agrees:true}).state,'missing'));
console.log(`PASS: ${checks} research-demo decision checks`);
