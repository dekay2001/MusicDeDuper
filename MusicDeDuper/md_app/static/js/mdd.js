$(".SimilarTable").attr('cellpadding', '10');
$(".SimilarTable").attr('cellpadding', '10');



function BudgetDataManager(){
	//Expense List
	expeseList = [];
	incomeList = [];
	//Income List

	add_income = function(item){
		this.incomeList.push(item);
	}

	add_expense = function(item){
		this.expeseList.push(item);
	}
	//get_available_budget()
	get_available_budget = function(){
		return this.get_total_income() - this.get_total_expenses();
	}

	//get_total_expenses()
	get_total_expenses = function(){
		return _sumList(this.expenseList);
	}

	//get_total_income()
	get_total_income = function(){
		return _sumList(this.incomeList);
	}

	_sumList(dollar_list) = function(lineItemList){
		totalAmount = 0.0;
		for (var i = lineItemList.length - 1; i >= 0; i--) {
			//lineItemList[i]
			totalAmount += lineItemList[i].amount;
		}
		return totalAmount;
	}

}


function LineItem(description, amount){
	this.desc = description;
	this.amount = amount;
}


function BudgetController(bm){
	this.budgetManager = bm;
}

var bdm = new BudgetDataManager();
var bc = new BudgetController(bdm);