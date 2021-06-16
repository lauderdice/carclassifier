const API_METHODS = Object.freeze({POST:"POST", GET:"GET"})
const API_HOST = "http://127.0.0.1:5000"
const API_ENDPOINTS = Object.freeze({CLASSIFY: API_HOST+"/classify", CARDETAILS: API_HOST+"/cardetails"})
const FRONTEND_URL = 'http://localhost:63343'
class Utils {
		myRequest (url, method, body = null) {
			return new Promise((resolve, reject) => {
				const request = new XMLHttpRequest();
				request.addEventListener("load", e => {
					resolve(e);
				});
				request.addEventListener("error", e => {
					reject(e);
				});
				request.open(method, url);
				if (body === null){
					request.send();
				}else{
					request.send(formData);
				}
			});
		}


	static hideLoader(){
			let loader = document.getElementById("loader")
			loader.style.visibility = "hidden"
			let content = document.getElementById("content")
			content.style.visibility = "visible"
		}

	static displayLoader() {
			let loader = document.getElementById("loader")
			loader.style.visibility = "visible"
			let content = document.getElementById("content")
			content.style.visibility = "hidden"
		}
}
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
		this.currentPage = pageInstanceMatched ?? page404
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
	}

	render() {
		return homepageTemplate
	}

	pageShow() {
		super.pageShow()
		this.attachListeners()

	}
	attachListeners() {
		document.getElementById("findcartype-btn").addEventListener("click", function(event){
			event.preventDefault();
			console.log(event);
			var file = document.getElementById("inputGroupFile01").files[0];
			if (file === undefined) {
				alert("You have to select some file")
			} else{
				if (file["name"].split(".").pop() !== "jpg" && file["name"].split(".").pop() !== "JPG"
					&& file["name"].split(".").pop() !== "jpeg" && file["name"].split(".").pop() !== "JPEG"){
					alert("You have to select a jpeg file, not " + file["name"].split(".").pop())
				}else{
					try {
						Utils.displayLoader()
						localStorage.setItem("file", file);
						var form = document.getElementById("CarImageForm");
						var formData = new FormData(form);
						var request = new XMLHttpRequest();
						request.onload = function() {
							console.log(request.responseText);
							localStorage.setItem("classification_result", request.responseText);
							let curr_url = new URL(window.location.href)
							globalRouter.route(curr_url.origin + curr_url.pathname + "?page=result")
							document.location.href = curr_url.origin + curr_url.pathname + "?page=result";
							Utils.hideLoader()
						};
						request.onerror = function() {
							alert("API is Not Connected, you will have to try later");
							Utils.hideLoader();
						}
						request.open(API_METHODS.POST, API_ENDPOINTS.CLASSIFY);
						request.setRequestHeader('Accept',"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
						request.send(formData);
					}catch (error){
						alert(error)
						Utils.hideLoader()
					}
				}

			}
		});
		$('#inputGroupFile01').on('change',function(){
			var fileName = $('input[type=file]').val().replace(/C:\\fakepath\\/i, '');
			$(this).next('.custom-file-label').html(fileName);
		})
	}
}

class PageClassificationResult extends Page {
	constructor(settings) {
		super(settings)
	}

	render() {
		return classificationresultTemplate
	}
	showClfResult(){
		let clfresult = JSON.parse(localStorage.getItem("classification_result"));
		let target = document.querySelector('#firstclf > h1');
		target.innerText = clfresult["result_1"]["prob"]
		target = document.querySelector('#firstclf > h3');
		target.innerText = clfresult["result_1"]["class"]

		target = document.querySelector('#secondclf > h1');
		target.innerText = clfresult["result_2"]["prob"]
		target = document.querySelector('#secondclf > h3');
		target.innerText = clfresult["result_2"]["class"]

		target = document.querySelector('#thirdclf > h1');
		target.innerText = clfresult["result_3"]["prob"]
		target = document.querySelector('#thirdclf > h3');
		target.innerText = clfresult["result_3"]["class"]

	}
	pageShow() {
		super.pageShow()
		this.showClfResult()
		this.attachListeners()
	}
	attachListeners() {
		document.querySelectorAll('a').forEach((element) => {
			element.addEventListener("click", function(event){
				event.preventDefault();
				Utils.displayLoader()
				let predictionId = this.attributes.href.value;
				let slctr = "#"+predictionId +" > h3"
				let car = document.querySelector(slctr).textContent
				var request = new XMLHttpRequest();
				request.onload = function() {
					console.log(request.responseText);
					localStorage.setItem("carinfo", request.responseText);
					let curr_url = new URL(window.location.href)
					globalRouter.route(curr_url.origin + curr_url.pathname + "?page=info")
					document.location.href = curr_url.origin + curr_url.pathname + "?page=info"
					Utils.hideLoader()
				};
				request.onerror = function() {
					alert("API is Not Connected, you will have to try later");
					Utils.hideLoader();
				}
				request.open(API_METHODS.GET, API_ENDPOINTS.CARDETAILS + "/" + car);
				request.setRequestHeader('Accept',"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
				request.send();
			})
		});

	}
	pageHide() {
		super.pageHide()
	}

}
class PageNotFound extends Page {
	constructor(settings) {
		super(settings)
	}

	render() {
		return `
			<h2>Not found</h2>
			<p>Unknown page</p>
			`
	}
	pageShow() {
		super.pageShow()
	}

	pageHide() {
		super.pageHide()
	}
}

class PageCarInformation extends Page {
	constructor(settings) {
		super(settings)
	}
	render() {
		return carinfoTemplate
	}
	pageShow() {
		super.pageShow()
		this.addCarInfoElements()
	}

	pageHide() {
		super.pageHide()
	}
	addCarInfoElements() {
		let review_container = document.getElementById("rev_container");
		let carinfo = JSON.parse(localStorage.getItem("carinfo"))
		let template = ""
		carinfo["reviews"].forEach(function(review) {
			template = template +  `
				<div class="p-2 align-content-center" style="max-width: 33%">
					<a href="` + review["url"] + `"><img style="max-width: 100%" src="` + review["thumbnail"] + `"></a>
					<h7 class="text-dark pt-0">` + review["title"] + `</h7>
				</div>
				`

		} )
		review_container.innerHTML = template
		let wiki = document.getElementById("wiki");
		wiki.innerText = carinfo["wiki"]
		let car = document.getElementById("carname");
		car.innerText = carinfo["car"] + " reviews"
		let body = document.querySelector("body")
		body.style.backgroundColor = "white"
		body.style.backgroundImage = "none"

	}
}
globalRouter = new Router({
    pages: [
        new PageHome({key: 'home', title: 'Homepage'}),
		new PageNotFound({key: '404', title: '404 - Not Found'}),
        new PageClassificationResult({key: 'result', title: 'Classification result'}),
		new PageCarInformation({key: 'info', title: 'Car Information'}),
	],
    defaultPage: 'home'
});