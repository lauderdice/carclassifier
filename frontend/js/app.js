
class Router {
	constructor({pages, defaultPage}) {
		this.pages = pages;
		this.defaultPage = defaultPage;
		this.currentPage = null

		// first run
		this.route(window.location.href);

		// listen on url changes from user clicking back button
		window.addEventListener('popstate', e => {
			this.route(window.location.href);
		});

		// listen on url changes from user clicks
		window.addEventListener('click', e => {
			const element = e.target
			if (element.nodeName === 'A') {
				e.preventDefault();
				this.route(element.href);
				window.history.pushState(null, null, element.href)
			}
		});
	}

	route(urlString) {
		const url = new URL(urlString)
		const page = url.searchParams.get('page')

		if (this.currentPage) {
			this.currentPage.pageHide()
		}

		const page404 = this.pages.find(p => p.key === '404')
		const pageInstanceMatched = this.pages.find(p => p.key === (page ?? this.defaultPage))
		const currentPage = pageInstanceMatched ?? page404

		this.currentPage = currentPage
		this.currentPage.pageShow()
	}
}

class Page {
	constructor({key, title}) {
		this.pageElement = document.querySelector(`#content`)
		this.title = title
		this.key = key
	}

	render() {
		return ``
	}

	pageShow() {
		this.pageElement.innerHTML = this.render()
		document.title = this.title
	}

	pageHide() {
		this.pageElement.innerHTML = ''
	}
}


class PageHome extends Page {
	constructor(settings) {
		super(settings)
		this.log = [];
	}

	render() {
		return homepageTemplate
	}

	pageShow() {
		super.pageShow()
		//this.logVisit();
		//this.showLog();
	}

	logVisit () {
		const date = new Date().toLocaleString("cs-CS");
		this.log.push(date);
		localStorage.setItem("log", JSON.stringify(this.log));
	}

	showLog () {
		const target = document.querySelector('#history-entries');

		target.innerHTML = ''
		for (const date of this.log) {
			const li = document.createElement('li');
			li.innerHTML = date;
			target.appendChild(li);
		}
	}
}

class PageClassificationResult extends Page {
	constructor(settings) {
		super(settings)
		this.log = null;
	}

	render() {
		return `
			<h2>Image Info</h2>

			<div id="dnd"></div>
			<ul id="imgInfo"></ul>
			<div id="imgCnt"></div>
		`
	}

	pageShow() {
		super.pageShow()

		const dnd = document.querySelector("#dnd");
		dnd.addEventListener("drop", this.onDrop);
		dnd.addEventListener("dragover", this.onDragOver);

	}

	pageHide() {
		dnd.removeEventListener("drop", this.onDrop);
		dnd.removeEventListener("dragover", this.onDragOver);

		super.pageHide()
	}

}

new Router({
    pages: [
        new PageHome({key: 'home', title: 'Homepage'}),
        new PageClassificationResult({key: 'result', title: 'Classification result'}),
    ],
    defaultPage: 'home'
});