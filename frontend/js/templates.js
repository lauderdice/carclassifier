
const homepageTemplate = `
<div class="h-100 container-fluid align-items-center">
    <div class="h-50 row row px-pd-n5 align-items-center" style="">
        <div class="col-sm-3"></div>
        <div class="col-sm-6">
            <h1 class="text-light mb-2">Welcome to CarClassifier.</h1>
            <h5 class="text-light mb-5">
                CarClassifier will help you find out the exact car type of an unknown car.
                Just upload a photo of a car and let it do its work
            </h5>
            <div class="row align-items-center">
                <div class="col-sm-1"></div>
                <div class="col-sm-10">
                    <form action="/classify" method=post encType=multipart/form-data id="CarImageForm" name="carfileform">
                        <div class="input-group">
                            <div class="custom-file">
                                <input type="file" name="carfile" class="custom-file-input" id="inputGroupFile01">
                                    <label class="custom-file-label" htmlFor="inputGroupFile01">Choose
                                        image&hellip;</label>
                            </div>
                            <div class="input-group-append">
                                <button class="btn btn-danger" id="findcartype-btn" type="submit">Find car type!</button>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="col-sm-1"></div>
            </div>

        </div>
        <div class="col-sm-3"></div>
    </div>
    <div class="h-50 row px-pd-n5 align-items-center" style="">
        <div class="col-sm-3"></div>
        <div class="col-sm-6">
            <div class="player">
              <video controls>
                <source src="media/schumacher.mp4" type="video/mp4">
                <source src="media/schumacher.mp4" type="video/mp4">
                <!-- fallback content here -->
              </video>
              <div class="controls">
                <button class="play" data-icon="P" aria-label="play pause toggle"></button>
                <button class="stop" data-icon="S" aria-label="stop"></button>
                <div class="timer">
                  <div></div>
                  <span aria-label="timer">00:00</span>
                </div>
                <button class="rwd" data-icon="B" aria-label="rewind"></button>
                <button class="fwd" data-icon="F" aria-label="fast forward"></button>
              </div>
            </div>
            <h2 style="text-align: center">..or, prior to running the neural network, you can listen to the Michael Schumacher song :) RIP</h2>

        </div>
        <div class="col-sm-3"></div>

</div>

<script>

</script>
`

const classificationresultTemplate =
    `
    <div class="h-100 container align-items-center">
        <div class="row px-pd-n5" style="height:15%"></div>
        <div class="h-25 row px-pd-n5" style="">
            <div class="col-sm-4" id="firstclf">
                <h1 class="text-light mb-2"></h1>
                <h3 class="text-light mb-2"></h3>
                <a href="firstclf">
                    <button class="btn btn-info">See car reviews and details</button>
                </a>
            </div>
            <div class="col-sm-4" id="secondclf">
                <h1 class="text-light mb-2"></h1>
                <h3 class="text-light mb-2"></h3>
                <a href="secondclf">
                    <button class="btn btn-info">See car reviews and details</button>
                </a>
            </div>
            <div class="col-sm-4" id="thirdclf">
                <h1 class="text-light mb-2"></h1>
                <h3 class="text-light mb-2"></h3>
                <a href="thirdclf">
                    <button class="btn btn-info">See car reviews and details</button>
                </a>
            </div>
        </div>
    </div>
`

const carinfoTemplate = `
<div class="container">
    <div class="row align-content-center my-4">
        <div class ="col-sm-4" >
            <h3 class="text-dark pt-2">CarClassifier Result</h3>
            <h4 class="text-dark pt-0" id="car"></h4>
            <a href="?page=result"><button class="btn btn-info">Back to results</button></a>
            <a href="?page=home"><button class="btn btn-danger">Homepage</button></a>
        </div>
        <div class ="col-sm-8">
            <h1 class="text-dark pt-0">Manufacturer - summary</h1>
            <p class="text-dark" id = "wiki"></p>
        </div>
    </div>
    <div class="row align-content-center my-4">
        <div class ="col-sm-12 text-center " >
            <h1 class="text-dark pt-0" id="carname"></h1>
        </div>

    </div>
</div>
<div class="container">
    <div class="d-flex flex-wrap" id="rev_container">
      
    </div>
</div>

`
