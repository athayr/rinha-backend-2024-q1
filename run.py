#!/usr/bin/env python
import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'src.main:app',
        host='0.0.0.0',
        port=9999,
        log_level='info',
        reload=True,
        reload_dirs=['src'],
        access_log=False,
        workers=True,
    )
