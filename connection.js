var elasticsearch=require('elasticsearch');

var client = new elasticsearch.Client( {  
	hosts: 'search-xingling-rt-twitter-map-2sqqiexw5xrhqcxx4x5o6d2a3y.us-west-2.es.amazonaws.com',
	connectionClass: require('http-aws-es'),
	amazonES:{
		region: 'us-west-2',
		accessKey: 'AKIAJLOM6B5SVN3TCLQQ',
		secretKey: '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'
	}
});

module.exports = client; 