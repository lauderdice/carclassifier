
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
                    <form action="/classify" method=post encType=multipart/form-data>
                        <div class="input-group">
                            <div class="custom-file">
                                <input type="file" name=file class="custom-file-input" id="inputGroupFile01">
                                    <label class="custom-file-label" htmlFor="inputGroupFile01">Choose
                                        image&hellip;</label>
                            </div>
                            <div class="input-group-append">
                                <button class="btn btn-danger" type="submit">Find car type!</button>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="col-sm-1"></div>
            </div>

        </div>

        <div class="col-sm-3"></div>
    </div>
</div>
`
